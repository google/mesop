import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {TextType} from 'mesop/mesop/components/text/text_jspb_proto_pb/mesop/components/text/text_pb';

@Component({
  selector: 'mesop-text',
  templateUrl: 'text.ng.html',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TextComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  _config!: TextType;

  ngOnChanges() {
    this._config = TextType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): TextType {
    return this._config;
  }
}
