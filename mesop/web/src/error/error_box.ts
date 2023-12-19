import {Component, Input} from '@angular/core';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {
  ServerError,
  StackFrame,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CommonModule} from '@angular/common';
import {ComponentRenderer} from '../component_renderer/component_renderer';
import {Channel} from '../services/channel';

@Component({
  selector: 'mesop-error-box',
  templateUrl: 'error_box.ng.html',
  styleUrl: 'error_box.css',
  standalone: true,
  imports: [CommonModule, ComponentRenderer, MatProgressBarModule],
  providers: [Channel],
})
export class ErrorBox {
  _showFullTraceback: boolean = false;
  _lastAppFrame: StackFrame | undefined;
  _hiddenErrors: Set<ServerError> = new Set();
  @Input({required: true}) error!: ServerError;

  isHidden(error: ServerError): boolean {
    return this._hiddenErrors.has(error);
  }

  hideError(error: ServerError): void {
    this._hiddenErrors.add(error);
  }

  ngOnChanges() {
    const traceback = this.error.getTraceback();
    if (!traceback) {
      return;
    }
    for (const frame of traceback.getFramesList().slice().reverse()) {
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
    const traceback = this.error.getTraceback();
    if (!traceback) {
      return false;
    }
    return traceback.getFramesList().every((frame) => !frame.getIsAppCode());
  }

  formatFrame(frame: StackFrame): string {
    return `${frame.getFilename()}:${frame.getLineNumber()} | ${frame.getCodeName()}`;
  }

  isLastAppCode(frame: StackFrame): boolean {
    return frame === this._lastAppFrame;
  }
}
