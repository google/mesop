import {Injectable, NgZone} from '@angular/core';
import {
  InitRequest,
  ServerError,
  States,
  UiRequest,
  UserEvent,
  Component as ComponentProto,
  UiResponse,
  NavigationEvent,
  ComponentConfig,
  EditorEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {Logger} from '../dev_tools/services/logger';
import {Title} from '@angular/platform-browser';
import {SSE} from '../utils/sse';

const anyWindow = window as any;
const DEV_SERVER_HOST = anyWindow['MESOP_SERVER_HOST'] || '';

interface InitParams {
  zone: NgZone;
  onRender: (
    rootComponent: ComponentProto,
    componentConfigs: ComponentConfig[],
  ) => void;
  onError: (error: ServerError) => void;
  onNavigate: (route: string) => void;
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
  private eventSource!: SSE;
  private initParams!: InitParams;
  private states!: States;
  private rootComponent?: ComponentProto;
  private status!: ChannelStatus;
  private componentConfigs: ComponentConfig[] = [];
  private queuedEvents: (() => void)[] = [];

  constructor(
    private logger: Logger,
    private title: Title,
  ) {}

  getStatus(): ChannelStatus {
    return this.status;
  }

  isHotReloading(): boolean {
    return this._isHotReloading;
  }

  getRootComponent(): ComponentProto | undefined {
    return this.rootComponent;
  }

  getComponentConfigs(): ComponentConfig[] {
    return this.componentConfigs;
  }

  init(initParams: InitParams, request?: UiRequest) {
    if (!request) {
      request = new UiRequest();
      request.setInit(new InitRequest());
    }
    this.eventSource = new SSE(`${DEV_SERVER_HOST}/ui`, {
      payload: generatePayloadString(request),
    });
    this.status = ChannelStatus.OPEN;
    this.logger.log({type: 'StreamStart'});

    const {zone, onRender, onError, onNavigate} = initParams;
    this.initParams = initParams;

    this.eventSource.addEventListener('message', (e) => {
      // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
      zone.run(() => {
        const data = (e as any).data;
        if (data === '<stream_end>') {
          this.eventSource.close();
          this.status = ChannelStatus.CLOSED;
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
          case UiResponse.TypeCase.RENDER: {
            this.states = uiResponse.getRender()!.getStates()!;
            const rootComponent = uiResponse.getRender()!.getRootComponent()!;
            for (const command of uiResponse.getRender()!.getCommandsList()) {
              const navigate = command.getNavigate();
              if (navigate) {
                onNavigate(navigate.getUrl()!);
              }
            }
            const title = uiResponse.getRender()!.getTitle();
            if (title) {
              this.title.setTitle(title);
            }
            this.rootComponent = rootComponent;
            this.componentConfigs = uiResponse
              .getRender()!
              .getComponentConfigsList();
            onRender(rootComponent, this.componentConfigs);
            this.logger.log({
              type: 'RenderLog',
              states: this.states,
              rootComponent: rootComponent,
            });
            break;
          }
          case UiResponse.TypeCase.ERROR:
            onError(uiResponse.getError()!);
            console.log('error', uiResponse.getError());
            break;
          case UiResponse.TypeCase.TYPE_NOT_SET:
            throw new Error(`Unhandled case for server event: ${uiResponse}`);
        }
      });
    });
  }

  dispatch(userEvent: UserEvent) {
    // Except for navigation user event, every user event should have
    // an event handler.
    if (!userEvent.getHandlerId() && !userEvent.getNavigation()) {
      // This is a no-op user event, so we don't send it.
      return;
    }
    const initUserEvent = () => {
      userEvent.setStates(this.states);
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

  dispatchEditorEvent(event: EditorEvent) {
    this.logger.log({type: 'EditorEventLog', editorEvent: event});
    const request = new UiRequest();
    request.setEditorEvent(event);
    this.init(this.initParams, request);
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
    userEvent.setNavigation(new NavigationEvent());
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
