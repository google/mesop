import {Component, Input} from '@angular/core';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {
  ServerError,
  StackFrame,
} from 'optic/optic/protos/ui_jspb_proto_pb/optic/protos/ui_pb';
import {CommonModule} from '@angular/common';
import {ComponentRenderer} from '../component_renderer/component_renderer';
import {Channel} from '../services/channel';

@Component({
  selector: 'optic-error-box',
  templateUrl: 'error_box.ng.html',
  styleUrl: 'error_box.css',
  standalone: true,
  imports: [CommonModule, ComponentRenderer, MatProgressBarModule],
  providers: [Channel],
})
export class ErrorBox {
  _showFullTraceback: boolean = false;
  _lastAppFrame: StackFrame | undefined;
  @Input({required: true}) error!: ServerError;

  ngOnChanges() {
    for (const frame of this.error
      .getTraceback()!
      .getFramesList()
      .slice()
      .reverse()) {
      if (frame.getIsAppCode()) {
        this._lastAppFrame = frame;
        return;
      }
    }
  }

  turnOnFullTraceBack() {
    this._showFullTraceback = true;
  }

  showFullTraceback() {
    if (this._showFullTraceback) {
      return true;
    }
    return this.error
      .getTraceback()!
      .getFramesList()
      .every((frame) => !frame.getIsAppCode());
  }

  formatFrame(frame: StackFrame): string {
    return `${frame.getFilename()}:${frame.getLineNumber()} | ${frame.getCodeName()}`;
  }

  isLastAppCode(frame: StackFrame): boolean {
    return frame === this._lastAppFrame;
  }
}
