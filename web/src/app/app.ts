import { Component, NgZone } from "@angular/core";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CommonModule } from "@angular/common";
import { ComponentRenderer } from "../component_renderer/component_renderer";
import { Channel, ChannelStatus } from "../services/channel";
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
import { DebugService } from "../dev_tools/services/debug_service";
import { Logger } from "../dev_tools/services/logger";
import { TypeDeserializer } from "../dev_tools/services/type_deserializer";

@Component({
  selector: "app",
  templateUrl: "app.ng.html",
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
    width: 420px;
  }

  `,
  providers: [DebugService, Channel, Logger, TypeDeserializer],
})
class App {
  rootComponent: pb.Component;
  error: pb.ServerError;

  constructor(
    private zone: NgZone,
    private channel: Channel,
    private iconRegistry: MatIconRegistry,
    private debugService: DebugService,
  ) {
    this.iconRegistry.setDefaultFontSetClass("material-symbols-rounded");
  }

  ngOnInit() {
    this.channel.init({
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
    return this.channel.getStatus() == ChannelStatus.OPEN;
  }

  showDebugButton() {
    return this.debugService.isDebugMode();
  }

  showRightSideNav() {
    return this.debugService.showDebugPanel();
  }

  toggleRightSideNav() {
    this.debugService.toggleShowDebugPanel();
  }
}

export function bootstrapApp() {
  bootstrapApplication(App, {
    providers: [provideAnimations()],
  });
}
