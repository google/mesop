import {Component, ElementRef, Input, ViewChild} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {EmbedType} from 'mesop/mesop/components/embed/embed_jspb_proto_pb/mesop/components/embed/embed_pb';
import {formatStyle} from '../../web/src/utils/styles';
import {
  setIframeSrc,
  setIframeSrcDoc,
} from '../../web/src/safe_iframe/safe_iframe';
import {DomSanitizer} from '@angular/platform-browser';

@Component({
  selector: 'mesop-embed',
  templateUrl: 'embed.ng.html',
  standalone: true,
})
export class EmbedComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  @ViewChild('iframe', {read: ElementRef}) iframe!: ElementRef;

  private _config!: EmbedType;
  private srcUrl!: string;
  private srcdoc!: string;

  constructor(private readonly sanitizer: DomSanitizer) {}

  ngOnChanges() {
    this._config = EmbedType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    const previousUrl = this.srcUrl;
    this.srcUrl = this._config.getSrc()!;
    const previousDoc = this.srcdoc;
    this.srcdoc = this._config.getHtml()!;

    // Reload iframe if the URL has changed.
    if (
      (this.srcUrl !== previousUrl || this.srcdoc !== previousDoc) &&
      this.iframe &&
      this.iframe.nativeElement
    ) {
      this.loadIframe();
    }
  }

  ngAfterViewInit() {
    this.loadIframe();
  }

  loadIframe() {
    if (this.srcUrl) {
      setIframeSrc(this.iframe.nativeElement, this.srcUrl);
    } else if (this.srcdoc) {
      setIframeSrcDoc(this.iframe.nativeElement, this.srcdoc, this.sanitizer);
    }
  }

  config(): EmbedType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
