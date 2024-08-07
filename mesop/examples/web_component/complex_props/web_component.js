import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class ComplexPropComponent extends LitElement {
  static properties = {
    array: {type: Array},
    object: {type: Object},
  };

  constructor() {
    super();
    this.array = [];
    this.object = {};
  }
  render() {
    return html`
      <div>
        <h3>Array Prop:</h3>
        <ul>
          ${this.array.map((item) => html`<li>${item}</li>`)}
        </ul>
        <h3>Object Prop:</h3>
        <ul>
          ${Object.entries(this.object).map(
            ([key, value]) => html` <li>${key}: ${value}</li> `,
          )}
        </ul>
      </div>
    `;
  }
}

customElements.define('complex-prop-component', ComplexPropComponent);
