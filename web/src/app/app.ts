import { Component, NgZone } from "@angular/core";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";
import { ChannelService, ChannelStatus } from "../services/channel_service";
import { ErrorBox } from "../error/error_box";
import {
  BrowserAnimationsModule,
  provideAnimations,
} from "@angular/platform-browser/animations";
import { bootstrapApplication } from "@angular/platform-browser";
import { MatIconModule, MatIconRegistry } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";
import { MatSidenavModule } from "@angular/material/sidenav";
import { DevTools } from "../dev_tools/dev_tools";

@Component({
  selector: "app",
  templateUrl: "app.html",
  standalone: true,
  imports: [
    CommonModule,
    ComponentRenderer,
    MatProgressBarModule,
    ErrorBox,
    DevTools,
    MatIconModule,
    MatButtonModule,
    MatSidenavModule,
  ],
  styles: `
  .container {
    height: 100%;
  }
  .debug-buttons {
    position: absolute;
    top: 0px;
    right: 0px;
  }
  .right-sidenav {
    width: 280px;
    padding: 16px;
  }

  `,
  providers: [ChannelService],
})
class App {
  rootComponent: pb.Component;
  error: pb.ServerError;
  rightSideNav: boolean;

  constructor(
    private zone: NgZone,
    private channelService: ChannelService,
    private iconRegistry: MatIconRegistry,
  ) {
    this.iconRegistry.setDefaultFontSetClass("material-symbols-rounded");
  }

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

  toggleRightSideNav() {
    this.rightSideNav = !this.rightSideNav;
    console.log("this.rightSideNav", this.rightSideNav);
  }
}

export function bootstrapApp() {
  bootstrapApplication(App, { providers: [provideAnimations()] });
}
