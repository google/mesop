import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class InnerComponent extends LitElement {
  static properties = {
    value: {type: Number},
    decrementEventHandlerId: {attribute: 'decrement-event', type: String},
  };

  constructor() {
    super();
    this.value = 0;
    this.decrementEventHandlerId = '';
  }

  render() {
    return html`
      <div class="container">
        <span>Value: ${this.value}</span>
        <button id="decrement-btn" @click="${this._onDecrement}">
          Decrement
        </button>
      </div>
    `;
  }

  _onDecrement() {
    this.dispatchEvent(
      new MesopEvent(this.decrementEventHandlerId, {
        value: this.value - 1,
      }),
    );
  }
}

customElements.define('inner-component', InnerComponent);
