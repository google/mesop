import {ChangeDetectorRef, Component, Input} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MarkdownType} from 'mesop/mesop/components/markdown/markdown_jspb_proto_pb/mesop/components/markdown/markdown_pb';
import {formatStyle} from '../../web/src/utils/styles';

@Component({
  selector: 'mesop-markdown',
  templateUrl: 'markdown.ng.html',
  standalone: true,
})
export class MarkdownComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;

  private _config!: MarkdownType;

  constructor(readonly changeDetectorRef: ChangeDetectorRef) {}

  async ngOnChanges() {
    this._config = MarkdownType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): MarkdownType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
