console.log('slow_component-start');
for (let i = 0; i < 10000000000; i++) {}
console.log('slow_component-end');

customElements.define(
  'slow-component',
  class extends HTMLElement {
    connectedCallback() {
      const paragraph = document.createElement('p');
      paragraph.textContent = 'Slow component';
      this.appendChild(paragraph);
    }
  },
);
