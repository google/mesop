import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class ScrollableComponent extends LitElement {
  renderRoot() {
    return this;
  }
  firstUpdated() {
    // this.focus();
  }
  render() {
    this.tabIndex = 0;
    this.style.overflowY = 'auto';
    this.style.outline = 'none';
  }
}

customElements.define('scrollable-component', ScrollableComponent);
