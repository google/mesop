import {Component, Input} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {HtmlType} from 'mesop/mesop/components/html/html_jspb_proto_pb/mesop/components/html/html_pb';
import {formatStyle} from '../../web/src/utils/styles';

@Component({
  selector: 'mesop-html',
  templateUrl: 'html.ng.html',
  standalone: true,
})
export class HtmlComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  private _config!: HtmlType;

  ngOnChanges() {
    this._config = HtmlType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): HtmlType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
