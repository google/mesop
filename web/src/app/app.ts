import { Component, NgZone } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";

// TODO: set this as environmental variable
const DEV_SERVER_URL = "http://127.0.0.1:8080/ui";

@Component({
  selector: "app",
  templateUrl: "app.html",
  standalone: true,
  imports: [CommonModule, ComponentRenderer],
})
export class App {
  rootComponent: pb.Component;

  constructor(private zone: NgZone) {}

  ngOnInit() {
    var eventSource = new EventSource(DEV_SERVER_URL);
    eventSource.onmessage = (e) => {
      // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
      this.zone.run(() => {
        console.log(e.data);
        const array = toUint8Array(atob(e.data));
        const serverEvent = pb.ServerEvent.deserializeBinary(array);
        switch (serverEvent.getTypeCase()) {
          case pb.ServerEvent.TypeCase.RENDER:
            this.rootComponent = serverEvent.getRender()!.getRootComponent()!;
            break;
          case pb.ServerEvent.TypeCase.TYPE_NOT_SET:
            throw new Error("Unhandled case for server event: " + serverEvent);
        }
      });
    };
  }
}

function toUint8Array(byteString: string): Uint8Array {
  const byteArray = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    byteArray[i] = byteString.charCodeAt(i);
  }
  return byteArray;
}
