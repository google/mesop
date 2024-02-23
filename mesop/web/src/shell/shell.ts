import {
  Component,
  ErrorHandler,
  HostListener,
  NgZone,
  Renderer2,
} from '@angular/core';
import {Router, RouterOutlet, Routes, provideRouter} from '@angular/router';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {
  ServerError,
  Component as ComponentProto,
  UserEvent,
  ComponentConfig,
  NavigationEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CommonModule} from '@angular/common';
import {ComponentRenderer} from '../component_renderer/component_renderer';
import {Channel, ChannelStatus} from '../services/channel';
import {provideAnimations} from '@angular/platform-browser/animations';
import {bootstrapApplication} from '@angular/platform-browser';
import {MatIconModule, MatIconRegistry} from '@angular/material/icon';
import {EditorService} from '../services/editor_service';
import {MatSidenavModule} from '@angular/material/sidenav';
import {ErrorBox} from '../error/error_box';
import {GlobalErrorHandlerService} from '../services/global_error_handler';

@Component({
  selector: 'mesop-shell',
  templateUrl: 'shell.ng.html',
  standalone: true,
  imports: [
    CommonModule,
    ComponentRenderer,
    MatProgressBarModule,
    MatIconModule,
    MatSidenavModule,
    ErrorBox,
  ],
  providers: [{provide: ErrorHandler, useClass: GlobalErrorHandlerService}],
  styleUrl: 'shell.css',
})
export class Shell {
  rootComponent!: ComponentProto;
  errors: ServerError[] = [];
  componentConfigs: ComponentConfig[] = [];

  constructor(
    private zone: NgZone,
    private renderer: Renderer2,
    private channel: Channel,
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
      onRender: (rootComponent, componentConfigs) => {
        this.rootComponent = rootComponent;
        this.componentConfigs = componentConfigs;
      },
      onNavigate: (route) => {
        this.router.navigateByUrl(route);
      },
      onError: (error) => {
        this.errors.push(error);
      },
    });
  }

  /** Listen to browser navigation events (go back/forward). */
  @HostListener('window:popstate', ['$event'])
  onPopState(event: Event) {
    const userEvent = new UserEvent();
    userEvent.setNavigation(new NavigationEvent());
    this.channel.dispatch(userEvent);
  }

  showChannelProgressIndicator() {
    // Do not show it if channel is hot reloading to reduce visual noise.
    return (
      this.channel.getStatus() === ChannelStatus.OPEN &&
      !this.channel.isHotReloading()
    );
  }
}

const routes: Routes = [{path: '**', component: Shell}];

@Component({
  selector: 'mesop-app',
  template: '<router-outlet></router-outlet>',
  standalone: true,
  imports: [Shell, RouterOutlet],
  providers: [EditorService],
})
class MesopApp {}

export function bootstrapApp() {
  bootstrapApplication(MesopApp, {
    providers: [provideAnimations(), provideRouter(routes)],
  });
}
