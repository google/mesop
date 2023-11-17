import { Component, Input } from "@angular/core";
import { Type } from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { TextType } from "optic/optic/components/text/text_ts_proto_pb/optic/components/text/text_pb";

@Component({
  selector: "app-text",
  templateUrl: "text.html",
  standalone: true,
})
export class TextComponent {
  @Input() type!: Type;
  _config: TextType;

  ngOnChanges() {
    this._config = TextType.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): TextType {
    return this._config;
  }
}
