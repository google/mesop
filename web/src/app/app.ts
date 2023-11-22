import { Component, NgZone } from "@angular/core";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";
import { ChannelService, ChannelStatus } from "../services/channel_service";

@Component({
  selector: "app",
  templateUrl: "app.html",
  styles: `
  .error {
    background-color: #ffe8ef;
    padding: 18px;
    color: #ae2626;
  }

  .exception {
    font-size: 1.5rem;
    font-weight: 500;
    padding-bottom: 16px;
    white-space: preserve;
  }

  .exception-title {
    font-weight: bold;
  }

  .traceback-heading {
    font-weight: 500;
    font-size: 1.2rem;
  }

  .traceback {
    font-family: monospace;
    font-size: 1rem;
    line-height: 1.5;
    white-space: preserve;
    border: 1.5px solid #d8adad;
    padding: 8px;
    border-radius: 12px;
    margin: 8px 0;
  }

  .traceback-segment {
    color: #444;
    margin-bottom: 12px;
  }

  .traceback-segment.highlight {
    color: #000;
    font-weight: bold;
  }

  .show-full-traceback {
    text-decoration: underline;
    font-size: 1rem;
  }

  .show-full-traceback:hover {
    cursor: pointer;
  }

  .status {
    height: 8px;
  }
  `,
  standalone: true,
  imports: [CommonModule, ComponentRenderer, MatProgressBarModule],
  providers: [ChannelService],
})
export class App {
  rootComponent: pb.Component;
  error: pb.ServerError;
  _tracebackSegments: TracebackSegment[];
  _showFullTraceback: boolean = false;

  constructor(
    private zone: NgZone,
    private channelService: ChannelService,
  ) {}

  ngOnInit() {
    this.channelService.init({
      zone: this.zone,
      onRender: (rootComponent) => {
        this.rootComponent = rootComponent;
      },
      onError: (error) => {
        this.error = error;
        this._tracebackSegments = processError(error);
      },
    });
  }

  isConnectionOpen() {
    return this.channelService.getStatus() == ChannelStatus.OPEN;
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
