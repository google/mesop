import { ChangeDetectionStrategy, Component, Input } from "@angular/core";
import {
  Key,
  Type,
} from "optic/optic/protos/ui_jspb_proto_pb/optic/protos/ui_pb";
import { TextType } from "optic/optic/components/text/text_jspb_proto_pb/optic/components/text/text_pb";

@Component({
  selector: "optic-text",
  templateUrl: "text.ng.html",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TextComponent {
  @Input({ required: true }) type!: Type;
  @Input() key!: Key;
  _config!: TextType;

  ngOnChanges() {
    this._config = TextType.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): TextType {
    return this._config;
  }
}
