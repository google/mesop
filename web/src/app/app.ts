import { Component, NgZone } from "@angular/core";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";
import { ChannelService, ChannelStatus } from "../services/channel_service";
import { ErrorBox } from "../error/error_box";

@Component({
  selector: "app",
  templateUrl: "app.html",
  standalone: true,
  imports: [CommonModule, ComponentRenderer, MatProgressBarModule, ErrorBox],
  providers: [ChannelService],
})
export class App {
  rootComponent: pb.Component;
  error: pb.ServerError;

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
      },
    });
  }

  isConnectionOpen() {
    return this.channelService.getStatus() == ChannelStatus.OPEN;
  }
}
