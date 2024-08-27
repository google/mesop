import {EditorView, basicSetup} from 'codemirror';
import {python} from '@codemirror/lang-python';
import {unifiedMergeView} from '@codemirror/merge';
import {EditorState} from '@codemirror/state';
import {oneDark} from '@codemirror/theme-one-dark';

import {
  Component,
  ElementRef,
  Input,
  Output,
  EventEmitter,
} from '@angular/core';

@Component({
  selector: 'mesop-code-mirror-diff',
  template: '',
  standalone: true,
})
export class CodeMirrorDiffComponent {
  @Input() beforeCode!: string;
  @Input() afterCode!: string;
  @Output() codeChange = new EventEmitter<string>();
  view: EditorView | null = null;
  constructor(private elementRef: ElementRef) {}

  ngOnChanges() {
    if (this.view) {
      this.view.destroy();
    }
    this.renderEditor();
  }

  renderEditor() {
    const extensions = [
      basicSetup,
      python(),
      EditorView.editable.of(false),
      EditorView.lineWrapping,
      unifiedMergeView({
        original: this.beforeCode,
        highlightChanges: true,
        mergeControls: false,
        gutter: true,
        collapseUnchanged: {margin: 2},
      }),
    ];

    if (document.body.classList.contains('dark-theme')) {
      extensions.push(oneDark);
    }

    this.view = new EditorView({
      state: EditorState.create({
        doc: this.afterCode,
        extensions,
      }),
      parent: this.elementRef.nativeElement,
    });
  }
}

@Component({
  selector: 'mesop-code-mirror-raw',
  template: '',
  standalone: true,
})
export class CodeMirrorRawComponent {
  @Input() code!: string | null;
  private view: EditorView | null = null;

  constructor(private elementRef: ElementRef) {}

  ngOnChanges() {
    if (this.view) {
      this.view.destroy();
    }
    this.renderEditor();
  }

  renderEditor() {
    const extensions = [
      basicSetup,
      python(),
      EditorView.editable.of(false),
      EditorView.lineWrapping,
    ];

    if (document.body.classList.contains('dark-theme')) {
      extensions.push(oneDark);
    }

    this.view = new EditorView({
      state: EditorState.create({
        doc: this.code ?? '',
        extensions,
      }),
      parent: this.elementRef.nativeElement,
    });
  }
}
