import { Component, Input } from "@angular/core";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";
import { ChannelService } from "../services/channel_service";

@Component({
  selector: "optic-error-box",
  templateUrl: "error_box.html",
  styleUrl: "error_box.css",
  standalone: true,
  imports: [CommonModule, ComponentRenderer, MatProgressBarModule],
  providers: [ChannelService],
})
export class ErrorBox {
  _showFullTraceback: boolean = false;

  @Input({ required: true }) error!: pb.ServerError;

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

  formatFrame(frame: pb.StackFrame): string {
    return `${frame.getFilename()}:${frame.getLineNumber()} | ${frame.getCodeName()}`;
  }
}
