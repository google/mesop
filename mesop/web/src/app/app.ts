import {
  Component,
  ElementRef,
  ErrorHandler,
  HostListener,
  NgZone,
  Renderer2,
  ViewChild,
} from '@angular/core';
import {Router, RouterOutlet, Routes, provideRouter} from '@angular/router';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {
  ServerError,
  Component as ComponentProto,
  UserEvent,
  NavigationEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CommonModule} from '@angular/common';
import {ComponentRenderer} from '../component_renderer/component_renderer';
import {Channel, ChannelStatus} from '../services/channel';
import {ErrorBox} from '../error/error_box';
import {provideAnimations} from '@angular/platform-browser/animations';
import {bootstrapApplication} from '@angular/platform-browser';
import {MatIconModule, MatIconRegistry} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatSidenavModule} from '@angular/material/sidenav';
import {DevTools} from '../dev_tools/dev_tools';
import {DevToolsSettings} from '../dev_tools/services/dev_tools_settings';
import {
  HotReloadWatcher,
  IbazelHotReloadWatcher,
} from '../services/hot_reload_watcher';
import {GlobalErrorHandlerService} from '../services/global_error_handler';

@Component({
  selector: 'app',
  templateUrl: 'app.ng.html',
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
  providers: [
    {provide: ErrorHandler, useClass: GlobalErrorHandlerService},
    {provide: HotReloadWatcher, useClass: IbazelHotReloadWatcher},
  ],
  styleUrl: 'app_styles.css',
})
class App {
  rootComponent!: ComponentProto;
  errors: ServerError[] = [];
  @ViewChild('dragHandle', {read: ElementRef}) dragHandle!: ElementRef;
  private isDragging = false;
  @ViewChild('sidenav', {read: ElementRef}) sidenav!: ElementRef;
  @ViewChild('sidenavContent', {read: ElementRef})
  sidenavContent!: ElementRef;

  constructor(
    private zone: NgZone,
    private renderer: Renderer2,
    // Injecting to ensure it's loaded in the app
    private hotReloadWatcher: HotReloadWatcher,
    private channel: Channel,
    private devToolsSettings: DevToolsSettings,
    iconRegistry: MatIconRegistry,
    private router: Router,
    errorHandler: ErrorHandler,
  ) {
    iconRegistry.setDefaultFontSetClass('material-symbols-rounded');
    (errorHandler as GlobalErrorHandlerService).setOnError((error) => {
      const errorProto = new ServerError();
      errorProto.setException(`JS Error: ${error.toString()}`);
      this.errors.push(errorProto);
    });
  }

  ngOnInit() {
    this.channel.init({
      zone: this.zone,
      onRender: (rootComponent) => {
        this.rootComponent = rootComponent;
      },
      onNavigate: (route) => {
        this.router.navigateByUrl(route);
      },
      onError: (error) => {
        this.errors.push(error);
      },
    });
  }

  ngAfterViewInit() {
    this.dragHandle.nativeElement.addEventListener('mousedown', () => {
      this.isDragging = true;
    });

    this.renderer.listen(document, 'mousemove', (event) => {
      if (!this.isDragging) return;

      const newWidth = window.innerWidth - event.clientX;
      this.sidenav.nativeElement.style.width = `${newWidth}px`;
      this.sidenavContent.nativeElement.style.marginRight = `${newWidth}px`;
    });

    this.renderer.listen(document, 'mouseup', (event) => {
      this.isDragging = false;
    });
  }

  /** Listen to browser navigation events (go back/forward). */
  @HostListener('window:popstate', ['$event'])
  onPopState(event: Event) {
    const userEvent = new UserEvent();
    userEvent.setNavigation(new NavigationEvent());
    this.channel.dispatch(userEvent);
  }

  isConnectionOpen() {
    return this.channel.getStatus() === ChannelStatus.OPEN;
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

const routes: Routes = [{path: '**', component: App}];

@Component({
  selector: 'optic-app',
  template: '<router-outlet></router-outlet>',
  standalone: true,
  imports: [App, RouterOutlet],
})
class OpticShell {}

export function bootstrapApp() {
  bootstrapApplication(OpticShell, {
    providers: [provideAnimations(), provideRouter(routes)],
  });
}
