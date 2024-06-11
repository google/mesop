class FooComponent extends HTMLElement {
  constructor() {
    super();
    this._shadowRoot = this.attachShadow({mode: 'open'});
    this._value = 0;
    this._style = '';
    this._incrementHandlerId = '';
    this._render();
  }

  static get observedAttributes() {
    return ['value', 'style', 'handler-id'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      if (name === 'value') {
        this._value = Number(newValue);
      } else if (name === 'style') {
        this._style = newValue;
      } else if (name === 'handler-id') {
        this._incrementHandlerId = newValue;
      }
      this._render();
    }
  }

  _render() {
    this._shadowRoot.innerHTML = window.trustedHTMLFromStringBypass(`
        <div class="container" style="${this._style}">
          <span>Value: ${this._value}</span>
          <button id="increment-btn">Increment</button>
        </div>
      `);

    this._shadowRoot
      .getElementById('increment-btn')
      .addEventListener('click', this._onIncrement.bind(this));
  }

  _onIncrement() {
    this.dispatchEvent(
      new CustomEvent('mesop-event', {
        detail: {
          payload: {value: this._value + 2},
          handlerId: this._incrementHandlerId,
        },
        bubbles: true,
      }),
    );
  }
}

window.customElements.define('foo-component', FooComponent);
