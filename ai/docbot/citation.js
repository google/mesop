import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class CitationComponent extends LitElement {
  static styles = css`
    .container {
      background: var(--sys-surface-container-high);
      border-radius: 12px;
    }

    .container:hover {
      background: var(--sys-surface-container-highest);
    }
  `;

  static properties = {
    url: {type: String},
  };

  constructor() {
    super();
    this.url = '';
  }

  render() {
    return html`
      <div class="container" @click="${this._onClick}">
        <slot></slot>
      </div>
    `;
  }

  _onClick() {
    console.log('clicked', this.url);
    // TODO: send a message to the parent to open the url
  }
}

customElements.define('citation-component', CitationComponent);
