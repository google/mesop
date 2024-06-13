import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

const INCREMENT_EVENT = 'increment-event';

class FooComponent extends LitElement {
  static properties = {
    value: {type: Number},
    style: {type: String},
    incrementEventHandlerId: {attribute: INCREMENT_EVENT, type: String},
  };

  constructor() {
    super();
    this.value = 0;
    this.style = '';
    this.incrementEventHandlerId = '';
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
          Increment2
        </button>
      </div>
    `;
  }

  _onIncrement() {
    debugger;
    this.dispatchEvent(
      new CustomEvent(INCREMENT_EVENT, {
        detail: {
          payload: {value: this.value + 2},
          handlerId: this.incrementEventHandlerId,
        },
        bubbles: true,
      }),
    );
  }
}

customElements.define('foo-component', FooComponent);
