import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';
import {VALUE} from './shared_module.js';

class SharedJsModuleComponent extends LitElement {
  render() {
    return html` <div>value from shared module: ${VALUE}</div> `;
  }
}

customElements.define('shared-js-module-component', SharedJsModuleComponent);
