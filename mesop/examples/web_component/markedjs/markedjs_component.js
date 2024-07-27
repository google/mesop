import {html, LitElement} from 'https://cdn.jsdelivr.net/npm/lit@3.1.4/+esm';
import {unsafeHTML} from 'https://cdn.jsdelivr.net/npm/lit@3.1.4/directives/unsafe-html.js/+esm';
import dompurify from 'https://cdn.jsdelivr.net/npm/dompurify@3.1.6/+esm';
import {Marked} from 'https://cdn.jsdelivr.net/npm/marked@13.0.2/+esm';
import {markedHighlight} from 'https://cdn.jsdelivr.net/npm/marked-highlight@2.1.3/+esm';
import highlightJs from 'https://cdn.jsdelivr.net/npm/highlight.js@11.10.0/+esm';
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/+esm';

/**
 * Markdown component using MarkedJS
 *
 * - HighlightJS used for code highlighting
 * - Mermaid JS integration for diagrams
 */
class MarkedJsComponent extends LitElement {
  static properties = {
    markdown: {type: String},
  };

  constructor() {
    super();
    mermaid.initialize({startOnLoad: true});
    this.marked = new Marked(
      markedHighlight({
        langPrefix: 'hljs language-',
        highlight(code, lang, info) {
          if (lang === 'mermaid') {
            return `<div class="mermaid">${code}</div>`;
          }
          const language = highlightJs.getLanguage(lang) ? lang : 'plaintext';
          return highlightJs.highlight(code, {language}).value;
        },
      }),
    );
  }

  createRenderRoot() {
    return this;
  }

  render() {
    return html`${unsafeHTML(
      dompurify.sanitize(this.marked.parse(this.markdown)),
    )}`;
  }
}

customElements.define('markedjs-component', MarkedJsComponent);
