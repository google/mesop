import {
  Component,
  DestroyRef,
  ElementRef,
  Input,
  ViewChild,
} from '@angular/core';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {HtmlType} from 'mesop/mesop/components/html/html_jspb_proto_pb/mesop/components/html/html_pb';
import {formatStyle} from '../../web/src/utils/styles';
import {setIframeSrc} from '../../web/src/safe_iframe/safe_iframe';

@Component({
  selector: 'mesop-html',
  templateUrl: 'html.ng.html',
  standalone: true,
})
export class HtmlComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  @ViewChild('iframe', {read: ElementRef}) iframe!: ElementRef;
  private _config!: HtmlType;
  isSandboxed!: boolean;
  html!: string;

  constructor(private destroyRef: DestroyRef) {}

  ngOnChanges() {
    this._config = HtmlType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    this.isSandboxed = this._config.getMode() === 'sandboxed';
    if (!this.isSandboxed) {
      return;
    }
    const previousHtml = this.html;
    this.html = this._config.getHtml()!;
    // Reload iframe if the HTML has changed.
    if (
      this.html !== previousHtml &&
      this.iframe &&
      this.iframe.nativeElement
    ) {
      this.loadIframe();
    }
  }

  ngAfterViewInit() {
    this.loadIframe();
  }

  loadIframe(): void {
    if (!this.iframe) {
      if (this.isSandboxed) {
        console.warn(
          'iframe element in Mesop html component unexpectedly not found',
        );
      }
      return;
    }
    const iframe = this.iframe.nativeElement as HTMLIFrameElement;
    // It's *critical* for web security isolation that allowSameOrigin is false
    // because sandbox_iframe.html is served from the main Mesop app origin
    // so we rely on iframe sandboxing to set this iframe to a null origin
    // (i.e. doesn't match any origin).
    //
    // Inside the iframe, we execute untrusted content which can include
    // user input.
    setIframeSrc(iframe, '/sandbox_iframe.html', {allowSameOrigin: false});
    iframe.onload = () => {
      const messageHandler = (event: MessageEvent) => {
        if (event.data?.type === 'mesopHtmlDimensions') {
          const iframe = this.iframe.nativeElement;
          // Explicitly cast event.data into number type just in case
          // the sandboxed iframe is trying to send malicious content.
          iframe.style.width = Number(event.data.width) + 'px';
          iframe.style.height = Number(event.data.height) + 'px';
        }
      };
      window.addEventListener('message', messageHandler);
      this.destroyRef.onDestroy(() => {
        window.removeEventListener('message', messageHandler);
      });

      iframe.contentWindow!.postMessage(
        {type: 'mesopExecHtml', html: this.html},
        '*', // targetOrigin is wildcard because it's given a null origin
      );
    };
  }

  config(): HtmlType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
