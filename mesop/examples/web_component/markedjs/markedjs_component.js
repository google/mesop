import {html, LitElement} from 'https://cdn.jsdelivr.net/npm/lit@3.1.4/+esm';
import {unsafeHTML} from 'https://cdn.jsdelivr.net/npm/lit@3.1.4/directives/unsafe-html.js/+esm';
import dompurify from 'https://cdn.jsdelivr.net/npm/dompurify@3.1.6/+esm';
import 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';

class MarkedJsComponent extends LitElement {
  static properties = {
    markdown: {type: String},
  };

  createRenderRoot() {
    return this;
  }

  render() {
    console.log();
    return html`${unsafeHTML(
      dompurify.sanitize(marked.parse(this.markdown), {
        // Set to false since we can't modify the trusted types in Mesop
        RETURN_TRUSTED_TYPE: false,
      }),
    )}`;
  }
}

customElements.define('markedjs-component', MarkedJsComponent);
