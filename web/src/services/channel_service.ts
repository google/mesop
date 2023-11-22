import { NgZone } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";

const anyWindow = window as any;
const DEV_SERVER_HOST = anyWindow["OPTIC_SERVER_HOST"] || "";

interface InitParams {
  zone: NgZone;
  onRender: (rootComponent: pb.Component) => void;
  onError: (error: pb.ServerError) => void;
}

export enum ChannelStatus {
  OPEN = "OPEN",
  CLOSED = "CLOSED",
}

export class ChannelService {
  private eventSource: EventSource;
  private initParams: InitParams;
  private state: pb.State;
  private status: ChannelStatus;

  constructor() {
    const request = new pb.UiRequest();
    request.setInit(new pb.InitRequest());
    this.eventSource = new EventSource(generateRequestUrl(request));
    this.status = ChannelStatus.OPEN;
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
          return;
        }

        const array = toUint8Array(atob(e.data));
        const UiResponse = pb.UiResponse.deserializeBinary(array);
        console.debug("Server event: ", UiResponse.toObject());
        switch (UiResponse.getTypeCase()) {
          case pb.UiResponse.TypeCase.RENDER:
            this.state = UiResponse.getRender()!.getState()!;

            onRender(UiResponse.getRender()!.getRootComponent()!);
            break;
          case pb.UiResponse.TypeCase.ERROR:
            onError(UiResponse.getError()!);
            console.log("error", UiResponse.getError());
            break;
          case pb.UiResponse.TypeCase.TYPE_NOT_SET:
            throw new Error("Unhandled case for server event: " + UiResponse);
        }
      });
    };
  }

  dispatch(userEvent: pb.UserEvent) {
    userEvent.setState(this.state);
    const request = new pb.UiRequest();
    request.setUserEvent(userEvent);

    this.eventSource.close();
    this.eventSource = new EventSource(generateRequestUrl(request));
    this.status = ChannelStatus.OPEN;
    this.init(this.initParams);
  }
}

function generateRequestUrl(request: pb.UiRequest): string {
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
