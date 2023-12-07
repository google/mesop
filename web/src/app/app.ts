import {
  Component,
  ElementRef,
  NgZone,
  Renderer2,
  ViewChild,
} from "@angular/core";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import {
  ServerError,
  Component as ComponentProto,
} from "optic/optic/protos/ui_jspb_proto_pb/optic/protos/ui_pb";
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
import { DevToolsSettings } from "../dev_tools/services/dev_tools_settings";
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

  .resize-handle {
    border: 0.75px solid gainsboro;
    border-radius: 1px;
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0px;
    width: 8px;
    cursor: ew-resize;
    z-index: 9999999;
    background: rgb(252, 252, 252);
  }
  `,
  providers: [DevToolsSettings, Channel, Logger, TypeDeserializer],
})
class App {
  rootComponent!: ComponentProto;
  error!: ServerError;
  @ViewChild("dragHandle", { read: ElementRef }) dragHandle!: ElementRef;
  private isDragging: boolean = false;
  @ViewChild("sidenav", { read: ElementRef }) sidenav!: ElementRef;
  @ViewChild("sidenavContent", { read: ElementRef })
  sidenavContent!: ElementRef;

  constructor(
    private zone: NgZone,
    private renderer: Renderer2,

    private channel: Channel,
    private iconRegistry: MatIconRegistry,
    private devToolsSettings: DevToolsSettings,
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

  ngAfterViewInit() {
    this.dragHandle.nativeElement.addEventListener("mousedown", () => {
      this.isDragging = true;
    });

    this.renderer.listen(document, "mousemove", (event) => {
      if (!this.isDragging) return;

      const newWidth = window.innerWidth - event.clientX;
      this.sidenav.nativeElement.style.width = `${newWidth}px`;
      this.sidenavContent.nativeElement.style.marginRight = `${newWidth}px`;
    });

    this.renderer.listen(document, "mouseup", (event) => {
      this.isDragging = false;
    });
  }

  isConnectionOpen() {
    return this.channel.getStatus() == ChannelStatus.OPEN;
  }

  showDebugButton() {
    return this.devToolsSettings.isDebugMode();
  }

  showDevTools() {
    return this.devToolsSettings.showDevTools();
  }

  toggleDevTools() {
    this.devToolsSettings.toggleShowDevTools();
  }
}

export function bootstrapApp() {
  bootstrapApplication(App, {
    providers: [provideAnimations()],
  });
}
