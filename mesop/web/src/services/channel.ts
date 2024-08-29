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

@Injectable({
  providedIn: 'root',
})
export class Channel {
  private _isHotReloading = false;
  private isWaiting = false;
  private isWaitingTimeout: number | undefined;
  private eventSource!: SSE;
  private initParams!: InitParams;
  private states: States = new States();
  private stateToken = '';
  private rootComponent?: ComponentProto;
  private status!: ChannelStatus;
  private componentConfigs: readonly ComponentConfig[] = [];
  private queuedEvents: (() => void)[] = [];
  private hotReloadBackoffCounter = 0;
  private hotReloadCounter = 0;

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
   * triggered by a user that's been taking a while. */
  isBusy(): boolean {
    return this.isWaiting && !this.isHotReloading();
  }

  getRootComponent(): ComponentProto | undefined {
    return this.rootComponent;
  }

  getComponentConfigs(): readonly ComponentConfig[] {
    return this.componentConfigs;
  }

  init(initParams: InitParams, request: UiRequest) {
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
      // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
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
        console.debug('Server event: ', uiResponse.toObject());
        switch (uiResponse.getTypeCase()) {
          case UiResponse.TypeCase.UPDATE_STATE_EVENT: {
            this.stateToken = uiResponse
              .getUpdateStateEvent()!
              .getStateToken()!;
            switch (uiResponse.getUpdateStateEvent()!.getTypeCase()) {
              case UpdateStateEvent.TypeCase.FULL_STATES: {
                this.states = uiResponse
                  .getUpdateStateEvent()!
                  .getFullStates()!;
                break;
              }
              case UpdateStateEvent.TypeCase.DIFF_STATES: {
                const states = uiResponse
                  .getUpdateStateEvent()!
                  .getDiffStates()!;

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
            const title = uiResponse.getRender()!.getTitle();
            if (title) {
              this.title.setTitle(title);
            }

            if (
              componentDiff !== undefined &&
              this.rootComponent !== undefined
            ) {
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
              this.experimentService.experimentalEditorToolbarEnabled =
                experimentSettings.getExperimentalEditorToolbarEnabled() ??
                false;
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
                request.getUserEvent()!.clearStateToken();
                request.getUserEvent()!.setStates(this.states);
                this.init(this.initParams, request);
              });
            } else {
              onError(uiResponse.getError()!);
              console.log('error', uiResponse.getError());
            }
            break;
          case UiResponse.TypeCase.TYPE_NOT_SET:
            throw new Error(`Unhandled case for server event: ${uiResponse}`);
        }
      });
    });
  }

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
      this.init(this.initParams, request);
    };
    this.logger.log({type: 'UserEventLog', userEvent: userEvent});
    if (this.status === ChannelStatus.CLOSED) {
      initUserEvent();
    } else {
      this.queuedEvents.push(() => {
        initUserEvent();
      });
    }
  }

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
    userEvent.setViewportSize(getViewportSize());
    userEvent.setNavigation(navigationEvent);
    userEvent.setQueryParamsList(getQueryParams());
    request.setUserEvent(userEvent);
    this.init(this.initParams, request);
  }
}

function generatePayloadString(request: UiRequest): string {
  request.setPath(window.location.pathname);
  const array = request.serializeBinary();
  const byteString = btoa(fromUint8Array(array))
    // Make this URL-safe:
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
  return byteString;
}

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

function toUint8Array(byteString: string): Uint8Array {
  const byteArray = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    byteArray[i] = byteString.charCodeAt(i);
  }
  return byteArray;
}
