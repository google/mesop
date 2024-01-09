import {Component, Input} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {TextType} from 'mesop/mesop/components/text/text_jspb_proto_pb/mesop/components/text/text_pb';
import {formatStyle} from '../../web/src/utils/styles';

@Component({
  selector: 'mesop-text',
  templateUrl: 'text.ng.html',
  standalone: true,
})
export class TextComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  _config!: TextType;

  getClass(): string {
    switch (this.config().getTypographyLevel()) {
      case TextType.TypographyLevel.H1:
        return 'mat-headline-1';
      case TextType.TypographyLevel.H2:
        return 'mat-headline-2';
      case TextType.TypographyLevel.H3:
        return 'mat-headline-3';
      case TextType.TypographyLevel.H4:
        return 'mat-headline-4';
      case TextType.TypographyLevel.H5:
        return 'mat-headline-5';
      case TextType.TypographyLevel.H6:
        return 'mat-headline-6';
      case TextType.TypographyLevel.SUBTITLE1:
        return 'mat-subtitle-1';
      case TextType.TypographyLevel.SUBTITLE2:
        return 'mat-subtitle-2';
      case TextType.TypographyLevel.BODY1:
        return 'mat-body-1';
      case TextType.TypographyLevel.BODY2:
        return 'mat-body-2';
      case TextType.TypographyLevel.CAPTION:
        return 'mat-caption';
    }
    return '';
  }

  ngOnChanges() {
    this._config = TextType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): TextType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
