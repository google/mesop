import {
  LitElement,
  html,
  css,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';
import 'https://cdn.plot.ly/plotly-2.32.0.min.js';

import {FOO} from './library.js';

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

    #plot {
      width: 100%;
      height: 100%;
    }
  `;

  createRenderRoot() {
    return this;
  }

  firstUpdated() {
    this.renderPlot();
  }

  renderPlot() {
    var trace1 = {
      x: [1, 2, 3, 4, 5],
      y: [10, 15, 13, 17, 21],
      type: 'scatter',
      mode: 'lines+markers',
      marker: {color: 'red'},
      name: 'Line 1',
    };

    var trace2 = {
      x: [1, 2, 3, 4, 5],
      y: [16, 5, 11, 9, 8],
      type: 'scatter',
      mode: 'lines+markers',
      marker: {color: 'blue'},
      name: 'Line 2',
    };

    var data = [trace1, trace2];

    var layout = {
      title: 'Simple Line Chart Example',
      xaxis: {
        title: 'X Axis',
      },
      yaxis: {
        title: 'Y Axis',
      },
    };

    Plotly.newPlot(document.getElementById('plot'), data, layout);
  }

  render() {
    return html`
      <div class="container" style="${this.style}">
        <div id="plot"></div>
        ${FOO}
        <span>Value: ${this.value}</span>
        <button id="increment-btn" @click="${this._onIncrement}">
          Increment
        </button>
      </div>
    `;
  }

  _onIncrement() {
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
