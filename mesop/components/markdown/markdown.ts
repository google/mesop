import {ChangeDetectorRef, Component, Input} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MarkdownType} from 'mesop/mesop/components/markdown/markdown_jspb_proto_pb/mesop/components/markdown/markdown_pb';
import {marked} from '../../web/external/marked';
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
  markdownHTML = '';

  private _config!: MarkdownType;
  isChecked = false;

  constructor(readonly changeDetectorRef: ChangeDetectorRef) {}

  async ngOnChanges() {
    this._config = MarkdownType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    this.markdownHTML = await marked.parse(this._config.getText()!);
    this.changeDetectorRef.detectChanges();
  }

  config(): MarkdownType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
