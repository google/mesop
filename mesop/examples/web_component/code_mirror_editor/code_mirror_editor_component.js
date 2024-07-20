import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

import 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.js';
import 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/mode/python/python.js';

class CodeMirrorEditorComponent extends LitElement {
  static properties = {
    code: {type: String},
    editorBlurEvent: {type: String},
    height: {type: String},
    width: {type: String},
  };

  constructor() {
    super();
    this.width = '100%';
    this.height = '100%';
    this.code = '';
    this.editor = null;
    this.editorState = null;
  }

  createRenderRoot() {
    return this;
  }

  firstUpdated() {
    this.renderEditor();
  }

  renderEditor() {
    this.editor = CodeMirror.fromTextArea(this.querySelector('#editor'), {
      mode: 'python',
      lineNumbers: true,
      theme: 'default',
      readOnly: false,
    });
    this.editor.setValue(this.code);
    this.editor.setSize(this.width, this.height);
    this.editor.on('blur', (cm) => {
      if (this.editorBlurEvent) {
        this.code = cm.getValue();
        this.dispatchEvent(
          new MesopEvent(this.editorBlurEvent, {
            code: this.code,
          }),
        );
      }
    });
  }

  updated(changedProperties) {
    if (changedProperties.has('code')) {
      if (this.code !== this.editor.getValue()) {
        this.editor.setValue(this.code);
      }
    }
  }

  render() {
    return html` <textarea id="editor"></textarea>`;
  }
}

customElements.define(
  'code-mirror-editor-component',
  CodeMirrorEditorComponent,
);
