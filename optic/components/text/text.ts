import { Component, Input } from "@angular/core";
import { Type } from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import * as pb from "optic/optic/components/text/text_ts_proto_pb/optic/components/text/text_pb";

@Component({
  selector: "app-text",
  templateUrl: "text.html",
  standalone: true,
})
export class TextComponent {
  @Input() data!: Type;

  getConfig(): pb.TextComponent {
    return pb.TextComponent.deserializeBinary(
      this.data.getValue() as Uint8Array,
    );
  }
}
