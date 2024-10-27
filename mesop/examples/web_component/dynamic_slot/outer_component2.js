import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class OuterComponent extends LitElement {
  render() {
    return html`
      <div class="container">
        &ltouter2&gt
        <slot></slot>
        &lt/outer2&gt
      </div>
    `;
  }
}

customElements.define('dynamic-slot-outer-component2', OuterComponent);
