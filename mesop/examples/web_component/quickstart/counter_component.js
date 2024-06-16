import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class CounterComponent extends LitElement {
  static properties = {
    value: {type: Number},
    decrementEvent: {type: String},
  };

  constructor() {
    super();
    this.value = 0;
    this.decrementEvent = '';
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
      new MesopEvent(this.decrementEvent, {
        value: this.value - 1,
      }),
    );
  }
}

customElements.define('quickstart-counter-component', CounterComponent);
