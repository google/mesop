import {Injectable, NgZone} from '@angular/core';
import {
  ServerError,
  States,
  UiRequest,
  UpdateStateEvent,
  UserEvent,
  Component as ComponentProto,
  UiResponse,
  NavigationEvent,
  ComponentConfig,
  Command,
  ChangePrefersColorScheme,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {Logger} from '../dev_tools/services/logger';
import {Title} from '@angular/platform-browser';
import {SSE} from '../utils/sse';
import {applyComponentDiff, applyStateDiff} from '../utils/diff';
import {getViewportSize} from '../utils/viewport_size';
import {ThemeService} from './theme_service';
import {getQueryParams} from '../utils/query_params';
import {ExperimentService} from './experiment_service';
import {io, Socket} from 'socket.io-client'; // Import Socket.IO client

// Pick 500ms as the minimum duration before showing a progress/busy indicator
// for the channel.
// See: https://github.com/google/mesop/issues/365
const WAIT_TIMEOUT_MS = 500;

interface InitParams {
  zone: NgZone;
  onRender: (
    rootComponent: ComponentProto,
    componentConfigs: readonly ComponentConfig[],
    jsModules: readonly string[],
  ) => void;
  onError: (error: ServerError) => void;
  onCommand: (command: Command) => void;
}

export enum ChannelStatus {
  OPEN = 'OPEN',
  CLOSED = 'CLOSED',
}

export enum ConnectionType {
  SSE = 'SSE',
  WEBSOCKET = 'WEBSOCKET',
}

@Injectable({
  providedIn: 'root',
})
export class Channel {
  private _isHotReloading = false;
  private isWaiting = false;
  private isWaitingTimeout: number | undefined;
  private eventSource!: SSE;
  private socket!: Socket;
  private initParams!: InitParams;
  private states: States = new States();
  private stateToken = '';
  private rootComponent?: ComponentProto;
  private status!: ChannelStatus;
  private componentConfigs: readonly ComponentConfig[] = [];
  private queuedEvents: (() => void)[] = [];
  private hotReloadBackoffCounter = 0;
  private hotReloadCounter = 0;
  private connectionType: ConnectionType = ConnectionType.SSE; // Default to SSE

  // Client-side state
  private overridedTitle = '';

  constructor(
    private logger: Logger,
    private title: Title,
    private themeService: ThemeService,
    private experimentService: ExperimentService,
  ) {
    this.themeService.setOnChangePrefersColorScheme(() => {
      const userEvent = new UserEvent();
      userEvent.setChangePrefersColorScheme(new ChangePrefersColorScheme());
      this.dispatch(userEvent);
    });
  }

  getStatus(): ChannelStatus {
    return this.status;
  }

  isHotReloading(): boolean {
    return this._isHotReloading;
  }

  /**
   * Return true if the channel has been doing work
   * triggered by a user that's been taking a while.
   */
  isBusy(): boolean {
    return this.isWaiting && !this.isHotReloading();
  }

  getRootComponent(): ComponentProto | undefined {
    return this.rootComponent;
  }

  getComponentConfigs(): readonly ComponentConfig[] {
    return this.componentConfigs;
  }

  /**
   * Initialize the channel with the given parameters and UI request.
   * Supports both SSE and WebSocket connections based on the `useWebSocket` flag.
   * @param initParams Initialization parameters.
   * @param request Initial UI request.
   * @param useWebSocket Whether to use WebSocket for the connection.
   */
  init(initParams: InitParams, request: UiRequest, useWebSocket = true) {
    this.connectionType = useWebSocket
      ? ConnectionType.WEBSOCKET
      : ConnectionType.SSE;

    if (this.connectionType === ConnectionType.SSE) {
      this.initSSE(initParams, request);
    } else {
      this.initWebSocket(initParams, request);
    }
  }

  /**
   * Initialize Server-Sent Events (SSE) connection.
   */
  private initSSE(initParams: InitParams, request: UiRequest) {
    this.eventSource = new SSE('/__ui__', {
      payload: generatePayloadString(request),
    });
    this.status = ChannelStatus.OPEN;
    this.isWaitingTimeout = setTimeout(() => {
      this.isWaiting = true;
    }, WAIT_TIMEOUT_MS);

    this.logger.log({type: 'StreamStart'});

    const {zone, onRender, onError, onCommand} = initParams;
    this.initParams = initParams;

    this.eventSource.addEventListener('message', (e) => {
      zone.run(() => {
        const data = (e as any).data;
        if (data === '<stream_end>') {
          this.eventSource.close();
          this.status = ChannelStatus.CLOSED;
          clearTimeout(this.isWaitingTimeout);
          this.isWaiting = false;
          this._isHotReloading = false;
          this.logger.log({type: 'StreamEnd'});
          if (this.queuedEvents.length) {
            const queuedEvent = this.queuedEvents.shift()!;
            queuedEvent();
          }
          return;
        }

        const array = toUint8Array(atob(data));
        const uiResponse = UiResponse.deserializeBinary(array);
        console.debug('Server event (SSE): ', uiResponse.toObject());
        this.handleUiResponse(uiResponse, onRender, onError, onCommand);
      });
    });

    this.eventSource.addEventListener('error', (e) => {
      zone.run(() => {
        console.error('SSE connection error:', e);
        this.status = ChannelStatus.CLOSED;
        this.eventSource.close();
      });
    });
  }

  /**
   * Initialize WebSocket connection using Socket.IO.
   */
  private initWebSocket(initParams: InitParams, request: UiRequest) {
    this.socket = io('/__ui__', {
      transports: ['websocket'],
      reconnectionAttempts: 5, // Adjust as needed
      // You can pass additional options here
    });

    this.status = ChannelStatus.OPEN;
    this.isWaitingTimeout = setTimeout(() => {
      this.isWaiting = true;
    }, WAIT_TIMEOUT_MS);

    this.logger.log({type: 'StreamStart'});

    const {zone, onRender, onError, onCommand} = initParams;
    this.initParams = initParams;

    this.socket.on('connect', () => {
      // Send the initial UiRequest upon connection
      const payload = generatePayloadString(request);
      this.socket.emit('message', payload);
    });

    this.socket.on('response', (data: any) => {
      zone.run(() => {
        if (data === '<stream_end>') {
          this.socket.disconnect();
          this.status = ChannelStatus.CLOSED;
          clearTimeout(this.isWaitingTimeout);
          this.isWaiting = false;
          this._isHotReloading = false;
          this.logger.log({type: 'StreamEnd'});
          if (this.queuedEvents.length) {
            const queuedEvent = this.queuedEvents.shift()!;
            queuedEvent();
          }
          return;
        }
        const prefix = 'data: ';

        const array = toUint8Array(atob(data.data.slice(prefix.length)));
        const uiResponse = UiResponse.deserializeBinary(array);
        console.debug('Server event (WebSocket): ', uiResponse.toObject());
        this.handleUiResponse(uiResponse, onRender, onError, onCommand);
      });
    });

    this.socket.on('error', (error: any) => {
      zone.run(() => {
        console.error('WebSocket error:', error);
        this.status = ChannelStatus.CLOSED;
      });
    });

    this.socket.on('disconnect', (reason: string) => {
      zone.run(() => {
        this.status = ChannelStatus.CLOSED;
        clearTimeout(this.isWaitingTimeout);
        this.isWaiting = false;
        this._isHotReloading = false;
      });
    });
  }

  /**
   * Handle UiResponse from the server.
   */
  private handleUiResponse(
    uiResponse: UiResponse,
    onRender: InitParams['onRender'],
    onError: InitParams['onError'],
    onCommand: InitParams['onCommand'],
  ) {
    switch (uiResponse.getTypeCase()) {
      case UiResponse.TypeCase.UPDATE_STATE_EVENT: {
        this.stateToken = uiResponse.getUpdateStateEvent()!.getStateToken()!;
        switch (uiResponse.getUpdateStateEvent()!.getTypeCase()) {
          case UpdateStateEvent.TypeCase.FULL_STATES: {
            this.states = uiResponse.getUpdateStateEvent()!.getFullStates()!;
            break;
          }
          case UpdateStateEvent.TypeCase.DIFF_STATES: {
            const states = uiResponse.getUpdateStateEvent()!.getDiffStates()!;

            const numDiffStates = states.getStatesList().length;
            const numStates = this.states.getStatesList().length;

            if (numDiffStates !== numStates) {
              throw Error(
                `Number of diffs (${numDiffStates}) doesn't equal the number of states (${numStates}))`,
              );
            }

            // `this.states` should be populated at this point since the first update
            // from the server should be the full state.
            for (let i = 0; i < numDiffStates; ++i) {
              const state = applyStateDiff(
                this.states.getStatesList()[i].getData() as string,
                states.getStatesList()[i].getData() as string,
              );
              this.states.getStatesList()[i].setData(state);
            }
            break;
          }
          case UpdateStateEvent.TypeCase.TYPE_NOT_SET:
            throw new Error('No state event data set');
        }
        break;
      }
      case UiResponse.TypeCase.RENDER: {
        const rootComponent = uiResponse.getRender()!.getRootComponent()!;
        const componentDiff = uiResponse.getRender()!.getComponentDiff()!;

        for (const command of uiResponse.getRender()!.getCommandsList()) {
          onCommand(command);
        }

        const title = this.overridedTitle || uiResponse.getRender()!.getTitle();
        if (title) {
          this.title.setTitle(title);
        }

        if (componentDiff !== undefined && this.rootComponent !== undefined) {
          // Angular does not update the UI if we apply the diff on the root
          // component instance which is why we create copy of the root component
          // first.
          const rootComponentToUpdate = ComponentProto.deserializeBinary(
            this.rootComponent.serializeBinary(),
          );
          applyComponentDiff(rootComponentToUpdate, componentDiff);
          this.rootComponent = rootComponentToUpdate;
        } else {
          this.rootComponent = rootComponent;
        }
        const experimentSettings = uiResponse
          .getRender()!
          .getExperimentSettings();
        if (experimentSettings) {
          this.experimentService.concurrentUpdatesEnabled =
            experimentSettings.getConcurrentUpdatesEnabled() ?? false;
          this.experimentService.experimentalEditorToolbarEnabled =
            experimentSettings.getExperimentalEditorToolbarEnabled() ?? false;
        }

        this.componentConfigs = uiResponse
          .getRender()!
          .getComponentConfigsList();
        onRender(
          this.rootComponent,
          this.componentConfigs,
          uiResponse.getRender()!.getJsModulesList(),
        );
        this.logger.log({
          type: 'RenderLog',
          states: this.states,
          rootComponent: this.rootComponent,
        });
        break;
      }
      case UiResponse.TypeCase.ERROR:
        if (
          uiResponse.getError()?.getException() ===
          'Token not found in state session backend.'
        ) {
          this.queuedEvents.unshift(() => {
            console.warn(
              'Token not found in state session backend. Retrying user event.',
            );
            // Assuming you have access to the original request here
            // If not, you might need to store it elsewhere
            const request = new UiRequest();
            const userEvent = new UserEvent();
            userEvent.clearStateToken();
            userEvent.setStates(this.states);
            request.setUserEvent(userEvent);
            this.init(
              this.initParams,
              request,
              this.connectionType === ConnectionType.WEBSOCKET,
            );
          });
        } else {
          onError(uiResponse.getError()!);
          console.log('error', uiResponse.getError());
        }
        break;
      case UiResponse.TypeCase.TYPE_NOT_SET:
        throw new Error(`Unhandled case for server event: ${uiResponse}`);
    }
  }

  /**
   * Dispatch a user event to the server.
   * Supports both SSE and WebSocket based on the current connection type.
   */
  dispatch(userEvent: UserEvent) {
    // Every user event should have an event handler,
    // except for the ones below:
    if (
      !userEvent.getHandlerId() &&
      !userEvent.getNavigation() &&
      !userEvent.getResize() &&
      !userEvent.getChangePrefersColorScheme()
    ) {
      // This is a no-op user event, so we don't send it.
      return;
    }
    const initUserEvent = () => {
      if (this.stateToken) {
        userEvent.setStateToken(this.stateToken);
      } else {
        userEvent.setStates(this.states);
      }
      // Make sure we compute these properties right before the user
      // event is dispatched, otherwise this can cause a weird
      // race condition.
      userEvent.setViewportSize(getViewportSize());
      userEvent.setThemeSettings(this.themeService.getThemeSettings());
      userEvent.setQueryParamsList(getQueryParams());

      const request = new UiRequest();
      request.setUserEvent(userEvent);
      this.init(
        this.initParams,
        request,
        this.connectionType === ConnectionType.WEBSOCKET,
      );
    };
    this.logger.log({type: 'UserEventLog', userEvent: userEvent});

    if (this.status === ChannelStatus.CLOSED) {
      initUserEvent();
    } else {
      this.queuedEvents.push(initUserEvent);
      if (this.experimentService.concurrentUpdatesEnabled) {
        // We will wait 1 second to see if the server will respond with a new state.
        // This addresses common use cases where a user may
        // type in a text input and then click a button and
        // they would expect the updated text input state to be
        // included in the click button event.
        setTimeout(() => {
          const initUserEventIndex = this.queuedEvents.findIndex(
            (event) => event === initUserEvent,
          );
          // The initUserEvent may have already been removed off the queue
          // if the response came back from the server already.
          if (initUserEventIndex !== -1) {
            const initUserEvent = this.queuedEvents.splice(
              initUserEventIndex,
              1,
            )[0];
            initUserEvent();
          }
        }, 1000);
      }
    }
  }

  /**
   * Check for hot reload by polling the server.
   */
  checkForHotReload() {
    const pollHotReloadEndpoint = async () => {
      try {
        const response = await fetch(
          `/__hot-reload__?counter=${this.hotReloadCounter}`,
        );
        if (response.status === 200) {
          const text = await response.text();
          this.hotReloadCounter = Number(text);
          this.hotReload();
          this.hotReloadBackoffCounter = 0;
          // Use void to explicitly not await to avoid downstream sync issue.
          void pollHotReloadEndpoint();
        } else {
          throw new Error(`Server responded with status: ${response.status}`);
        }
      } catch (error) {
        console.error('Hot reload polling error:', error);
        setTimeout(pollHotReloadEndpoint, this.calculateExponentialBackoff());
      }
    };

    pollHotReloadEndpoint();
  }

  private calculateExponentialBackoff(): number {
    const delay = 2 ** this.hotReloadBackoffCounter * 100;
    this.hotReloadBackoffCounter++;
    return delay;
  }

  resetOverridedTitle() {
    this.overridedTitle = '';
  }

  setOverridedTitle(newTitle: string) {
    this.overridedTitle = newTitle;
  }

  /**
   * Trigger a hot reload by sending a navigation event to the server.
   */
  hotReload() {
    // Only hot reload if there's no request in-flight.
    // Most likely the in-flight request will receive the updated UI.
    // In the unlikely chance it doesn't, we will wait for the next
    // hot reload trigger which is not ideal but acceptable.
    if (this.getStatus() === ChannelStatus.OPEN) {
      return;
    }
    this._isHotReloading = true;
    const request = new UiRequest();
    const userEvent = new UserEvent();
    userEvent.setStates(this.states);
    const navigationEvent = new NavigationEvent();
    userEvent.setNavigation(navigationEvent);
    userEvent.setViewportSize(getViewportSize());
    userEvent.setThemeSettings(this.themeService.getThemeSettings());
    userEvent.setQueryParamsList(getQueryParams());
    request.setUserEvent(userEvent);
    this.init(
      this.initParams,
      request,
      this.connectionType === ConnectionType.WEBSOCKET,
    );
  }
}

/**
 * Generate a URL-safe base64 payload string from the UiRequest.
 */
function generatePayloadString(request: UiRequest): string {
  request.setPath(window.location.pathname);
  const array = request.serializeBinary();
  const byteString = btoa(fromUint8Array(array))
    // Make this URL-safe:
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
  return byteString;
}

/**
 * Convert a Uint8Array to a string.
 */
function fromUint8Array(array: Uint8Array): string {
  // Chunk this to avoid RangeError: Maximum call stack size exceeded
  let result = '';
  const chunkSize = 16384; // This size can be adjusted

  for (let i = 0; i < array.length; i += chunkSize) {
    const chunk = array.subarray(i, i + chunkSize);
    result += String.fromCodePoint(...(chunk as unknown as number[]));
  }

  return result;
}

/**
 * Convert a string to a Uint8Array.
 */
function toUint8Array(byteString: string): Uint8Array {
  const byteArray = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    byteArray[i] = byteString.charCodeAt(i);
  }
  return byteArray;
}
