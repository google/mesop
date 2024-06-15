import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class OuterComponent extends LitElement {
  static properties = {
    value: {type: Number},
    incrementEventHandlerId: {attribute: 'increment-event', type: String},
  };

  constructor() {
    super();
    this.value = 0;
    this.incrementEventHandlerId = '';
  }

  render() {
    return html`
      <div class="container">
        <span>Value: ${this.value}</span>
        <button id="increment-btn" @click="${this._onIncrement}">
          increment
        </button>
        Start of Slot:
        <slot></slot>
        End of Slot:
      </div>
    `;
  }

  _onIncrement() {
    this.dispatchEvent(
      new MesopEvent(this.incrementEventHandlerId, {
        value: this.value + 1,
      }),
    );
  }
}

customElements.define('outer-component', OuterComponent);
