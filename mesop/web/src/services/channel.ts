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
  private eventSource!: EventSource;
  private initParams!: InitParams;
  private states!: States;
  private status!: ChannelStatus;
  private queuedEvents: (() => void)[] = [];

  constructor(private logger: Logger) {}

  getStatus(): ChannelStatus {
    return this.status;
  }

  init(initParams: InitParams, request?: UiRequest) {
    if (!request) {
      request = new UiRequest();
      request.setInit(new InitRequest());
    }
    this.eventSource = new EventSource(generateRequestUrl(request));
    this.status = ChannelStatus.OPEN;
    this.logger.log({type: 'StreamStart'});

    const {zone, onRender, onError, onNavigate} = initParams;
    this.initParams = initParams;

    this.eventSource.onmessage = (e) => {
      // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
      zone.run(() => {
        if (e.data === '<stream_end>') {
          this.eventSource.close();
          this.status = ChannelStatus.CLOSED;
          this.logger.log({type: 'StreamEnd'});
          if (this.queuedEvents.length) {
            const queuedEvent = this.queuedEvents.shift()!;
            queuedEvent();
          }
          return;
        }

        const array = toUint8Array(atob(e.data));
        const uiResponse = UiResponse.deserializeBinary(array);
        console.debug('Server event: ', uiResponse.toObject());
        switch (uiResponse.getTypeCase()) {
          case UiResponse.TypeCase.RENDER: {
            this.states = uiResponse.getRender()!.getStates()!;
            const rootComponent = uiResponse.getRender()!.getRootComponent()!;
            for (const command of uiResponse.getRender()!.getCommandsList()) {
              const navigate = command.getNavigate();
              if (navigate) {
                onNavigate(navigate.getUrl());
              }
            }

            onRender(
              rootComponent,
              uiResponse.getRender()!.getComponentConfigsList(),
            );
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
    };
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
    const request = new UiRequest();
    const userEvent = new UserEvent();
    userEvent.setStates(this.states);
    userEvent.setNavigation(new NavigationEvent());
    request.setUserEvent(userEvent);
    this.init(this.initParams, request);
  }
}

function generateRequestUrl(request: UiRequest): string {
  request.setPath(window.location.pathname);
  const array = request.serializeBinary();
  const byteString = btoa(fromUint8Array(array))
    // Make this URL-safe:
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
  return `${DEV_SERVER_HOST}/ui?request=${byteString}`;
}

function fromUint8Array(array: Uint8Array): string {
  return String.fromCodePoint(...(array as unknown as number[]));
}

function toUint8Array(byteString: string): Uint8Array {
  const byteArray = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    byteArray[i] = byteString.charCodeAt(i);
  }
  return byteArray;
}
