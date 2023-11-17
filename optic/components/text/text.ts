import { Component, Input } from "@angular/core";
import { Type } from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import * as pb from "optic/optic/components/text/text_ts_proto_pb/optic/components/text/text_pb";

@Component({
  selector: "app-text",
  templateUrl: "text.html",
  standalone: true,
})
export class TextComponent {
  @Input() type!: Type;
  _config: pb.TextComponent;

  ngOnChanges() {
    this._config = pb.TextComponent.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): pb.TextComponent {
    return this._config;
  }
}
