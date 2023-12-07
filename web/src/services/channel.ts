import { Injectable, NgZone } from "@angular/core";
import {
  InitRequest,
  ServerError,
  States,
  UiRequest,
  UserEvent,
  Component as ComponentProto,
  UiResponse,
} from "optic/optic/protos/ui_jspb_proto_pb/optic/protos/ui_pb";
import { Logger } from "../dev_tools/services/logger";

const anyWindow = window as any;
const DEV_SERVER_HOST = anyWindow["OPTIC_SERVER_HOST"] || "";

interface InitParams {
  zone: NgZone;
  onRender: (rootComponent: ComponentProto) => void;
  onError: (error: ServerError) => void;
}

export enum ChannelStatus {
  OPEN = "OPEN",
  CLOSED = "CLOSED",
}

@Injectable()
export class Channel {
  private eventSource: EventSource;
  private initParams!: InitParams;
  private states!: States;
  private status: ChannelStatus;

  constructor(private logger: Logger) {
    const request = new UiRequest();
    request.setInit(new InitRequest());
    this.eventSource = new EventSource(generateRequestUrl(request));
    this.status = ChannelStatus.OPEN;
    this.logger.log({ type: "StreamStart" });
  }

  getStatus(): ChannelStatus {
    return this.status;
  }

  init(initParams: InitParams) {
    const { zone, onRender, onError } = initParams;
    this.initParams = initParams;

    this.eventSource.onmessage = (e) => {
      // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
      zone.run(() => {
        if (e.data == "<stream_end>") {
          this.eventSource.close();
          this.status = ChannelStatus.CLOSED;
          this.logger.log({ type: "StreamEnd" });
          return;
        }

        const array = toUint8Array(atob(e.data));
        const uiResponse = UiResponse.deserializeBinary(array);
        console.debug("Server event: ", uiResponse.toObject());
        switch (uiResponse.getTypeCase()) {
          case UiResponse.TypeCase.RENDER:
            this.states = uiResponse.getRender()!.getStates()!;
            const rootComponent = uiResponse.getRender()!.getRootComponent()!;
            onRender(rootComponent);
            this.logger.log({
              type: "RenderLog",
              states: this.states,
              rootComponent: rootComponent,
            });
            break;
          case UiResponse.TypeCase.ERROR:
            onError(uiResponse.getError()!);
            console.log("error", uiResponse.getError());
            break;
          case UiResponse.TypeCase.TYPE_NOT_SET:
            throw new Error("Unhandled case for server event: " + uiResponse);
        }
      });
    };
  }

  dispatch(userEvent: UserEvent) {
    userEvent.setStates(this.states);
    const request = new UiRequest();
    request.setUserEvent(userEvent);

    this.eventSource.close();
    this.eventSource = new EventSource(generateRequestUrl(request));
    this.status = ChannelStatus.OPEN;
    this.logger.log({ type: "StreamStart" });
    this.logger.log({ type: "UserEventLog", userEvent: userEvent });
    this.init(this.initParams);
  }
}

function generateRequestUrl(request: UiRequest): string {
  request.setPath(window.location.pathname);
  const array = request.serializeBinary();
  const byteString = btoa(fromUint8Array(array));
  return DEV_SERVER_HOST + "/ui?request=" + byteString;
}

function fromUint8Array(array: Uint8Array): string {
  let binary = "";
  for (let i = 0; i < array.length; i++) {
    binary += String.fromCharCode(array[i]);
  }
  return binary;
}

function toUint8Array(byteString: string): Uint8Array {
  const byteArray = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    byteArray[i] = byteString.charCodeAt(i);
  }
  return byteArray;
}
