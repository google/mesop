import {EditorView, basicSetup} from 'codemirror';
import {python} from '@codemirror/lang-python';
import {MergeView} from '@codemirror/merge';

import {
  Component,
  ElementRef,
  Input,
  Output,
  EventEmitter,
} from '@angular/core';

@Component({
  selector: 'mesop-code-mirror',
  template: '',
  standalone: true,
})
export class CodeMirrorComponent {
  @Input() beforeCode!: string;
  @Input() afterCode!: string;
  @Output() codeChange = new EventEmitter<string>();
  constructor(private elementRef: ElementRef) {}

  ngOnChanges() {
    while (this.elementRef.nativeElement.firstChild) {
      this.elementRef.nativeElement.firstChild.remove();
    }
    this.renderEditor();
  }

  renderEditor() {
    const mergeView = new MergeView({
      a: {
        doc: this.beforeCode,
        extensions: [
          basicSetup,
          python(),
          EditorView.editable.of(false),
          EditorView.lineWrapping,
        ],
      },
      b: {
        doc: this.afterCode,
        extensions: [
          basicSetup,
          python(),
          EditorView.editable.of(false),
          EditorView.lineWrapping,
        ],
      },
      parent: this.elementRef.nativeElement,
      highlightChanges: true,
      collapseUnchanged: {margin: 2},
      gutter: true,
    });
  }
}
