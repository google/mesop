import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class CitationComponent extends LitElement {
  static styles = css`
    a {
      display: block;
      text-decoration: none;
      color: var(--mat-sys-on-surface);
    }

    .container {
      background: var(--mat-sys-surface-container-high);
      border-radius: 12px;
    }

    .container:hover {
      background: var(--mat-sys-surface-container-highest);
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
      <a class="container" href="${this.url}" target="_blank">
        <slot></slot>
      </a>
    `;
  }

  _onClick() {
    window.open(this.url, '_blank');
    console.log('open url', this.url);
  }
}

customElements.define('citation-component', CitationComponent);
