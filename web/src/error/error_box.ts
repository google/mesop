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
  _tracebackSegments: TracebackSegment[];
  _showFullTraceback: boolean = false;

  @Input({ required: true }) error!: pb.ServerError;

  ngOnChanges() {
    this._tracebackSegments = processError(this.error);
  }

  turnOnFullTraceBack() {
    this._showFullTraceback = true;
  }

  showFullTraceback() {
    if (this._showFullTraceback) {
      return true;
    }
    return this._tracebackSegments.every((s) => s.type === "lowlight");
  }

  getTracebackSegments(): TracebackSegment[] {
    return this._tracebackSegments;
  }
}

interface TracebackSegment {
  text: string;
  type: "highlight" | "lowlight";
}

function getTypeFromPath(str: string): "highlight" | "lowlight" {
  // TODO: make this logic more robust.
  return str.includes("/examples/") ? "highlight" : "lowlight";
}

function processError(error: pb.ServerError): TracebackSegment[] {
  const originalTraceback = error
    .getTraceback()
    .slice("Traceback (most recent call last):".length)
    .trimStart();
  const regex = /File ".*?\.runfiles/g;

  const trimmedString = originalTraceback.replace(regex, 'File "/');

  const res = trimmedString
    .split("File")
    .map((str) => ({
      text: str.trimEnd(),
      type: getTypeFromPath(str),
    }))
    .slice(1) as TracebackSegment[];

  return res;
}
