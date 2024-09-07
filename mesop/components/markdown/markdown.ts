import {
  ChangeDetectorRef,
  Component,
  Input,
  ElementRef,
  Renderer2,
  SecurityContext,
} from '@angular/core';
import {DomSanitizer, SafeHtml} from '@angular/platform-browser';
import {marked} from 'marked';
import hljs from 'highlight.js';
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

  htmlOutput: SafeHtml = '';

  private _codeBlocks: string[] = [];
  private _config!: MarkdownType;

  constructor(
    readonly changeDetectorRef: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
    private renderer: Renderer2,
    private el: ElementRef,
  ) {}

  async ngOnChanges() {
    this._config = MarkdownType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );

    // Create a custom renderer so we can add highlighting and a copy button to code
    // blocks.
    //
    // We recreate the renderer each time the markdown gets updated, since we need to
    // keep track of the code blocks for the copy button.
    //
    const renderer = new marked.Renderer();
    this._codeBlocks = [];
    // We do not put the raw code in the HTML markup. Instead we just add the index of
    // the raw code to look up on click.
    let index = -1;
    renderer.code = ({text, lang}) => {
      const language =
        lang !== undefined && hljs.getLanguage(lang) ? lang : 'plaintext';
      const highlighted = hljs.highlight(text, {language}).value;
      this._codeBlocks.push(text);
      index += 1;
      // We use a <div class="code-${index}"></div> as a placeholder since Angular does
      // not allow buttons during HTML sanitization.
      return `<div class="code-block"><div class="code-${index}"></div><pre><code class="hljs ${language}">${highlighted}</code></pre></div>`;
    };

    // Use the custom renderer in Marked.js
    marked.use({renderer});

    const output = await marked(this._config!.getText()!, {gfm: true});

    // Sanitize the generated HTML from MarkedJS first.
    const html = this.sanitizer.sanitize(SecurityContext.HTML, output) || '';
    // Now update the placeholder div with our button once we know the output is
    // sanitized.
    this.htmlOutput = this.sanitizer.bypassSecurityTrustHtml(
      (html as string).replace(
        /<div class="code-(\d+)"><\/div>/g,
        '<button data-index="$1"><span role="img" class="mat-icon notranslate material-symbols-rounded mat-icon-no-color" aria-hidden="true" data-mat-icon-type="font">content_copy</span></button>',
      ),
    );
    // Need a small delay for the output to render before the click event handlers are
    // added.
    setTimeout(() => {
      this.addClickListener();
    }, 100);
  }

  addClickListener(): void {
    const buttons = this.el.nativeElement.querySelectorAll('button');
    // Use Renderer2 to safely bind a click event to the button
    for (const button of buttons) {
      this.renderer.listen(button, 'click', (e: Event) => {
        const target = e.currentTarget as HTMLElement;
        const dataText = target.getAttribute('data-index');
        if (dataText !== null) {
          navigator.clipboard.writeText(this._codeBlocks[parseInt(dataText)]);
        }
      });
    }
  }

  config(): MarkdownType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }
}
