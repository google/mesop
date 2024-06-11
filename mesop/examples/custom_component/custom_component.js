import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class FooComponent extends LitElement {
  static properties = {
    value: {type: Number},
    style: {type: String},
    handlerId: {type: String},
  };

  constructor() {
    super();
    this.value = 0;
    this.style = '';
    this.handlerId = '';
  }

  static styles = css`
    :host {
      display: block;
    }
  `;

  render() {
    return html`
      <div class="container" style="${this.style}">
        <span>Value: ${this.value}</span>
        <button id="increment-btn" @click="${this._onIncrement}">
          Increment
        </button>
      </div>
    `;
  }

  _onIncrement() {
    this.dispatchEvent(
      new CustomEvent('mesop-event', {
        detail: {
          payload: {value: this.value + 2},
          handlerId: this.handlerId,
        },
        bubbles: true,
      }),
    );
  }
}

customElements.define('foo-component', FooComponent);
