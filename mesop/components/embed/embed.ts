import {Component, ElementRef, Input, ViewChild} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {EmbedType} from 'mesop/mesop/components/embed/embed_jspb_proto_pb/mesop/components/embed/embed_pb';
import {formatStyle} from '../../web/src/utils/styles';
import {setIframeSrc} from '../../web/src/safe_iframe/safe_iframe';

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

  ngOnChanges() {
    this._config = EmbedType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    const previousUrl = this.srcUrl;
    this.srcUrl = this._config.getSrc()!;

    // Reload iframe if the URL has changed.
    if (
      this.srcUrl !== previousUrl &&
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
    if (this.srcUrl === '/sandbox_iframe.html') {
      throw new Error(
        "Dangerous to iframe sandbox_iframe.html. Use me.html(mode='sandboxed') instead.",
      );
    }
    // It's OK to allow same origin because if this.srcUrl is the
    // same origin as the Mesop app, then an attacker could navigate the user to
    // that URL directly to exploit the Mesop app's origin.
    // If this.srcUrl is another origin, then it will be treated as a
    // separate origin from the Mesop app origin even with allowSameOrigin: true.
    // Setting allowSameOrigin to true enables various functionalities
    // to work (e.g. cookies, local storage).
    setIframeSrc(this.iframe.nativeElement, this.srcUrl, {
      allowSameOrigin: true,
    });
  }

  config(): EmbedType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
