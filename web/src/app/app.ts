import { Component, NgZone } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";
import { ChannelService } from "../services/channel_service";

@Component({
  selector: "app",
  templateUrl: "app.html",
  standalone: true,
  imports: [CommonModule, ComponentRenderer],
  providers: [ChannelService],
})
export class App {
  rootComponent: pb.Component;

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
    });
  }
}
