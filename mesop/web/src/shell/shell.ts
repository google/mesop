import {Component, HostListener, NgZone, Renderer2} from '@angular/core';
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
import {EditorModeService} from '../services/editor_mode_service';

@Component({
  selector: 'mesop-shell',
  templateUrl: 'shell.ng.html',
  standalone: true,
  imports: [
    CommonModule,
    ComponentRenderer,
    MatProgressBarModule,
    MatIconModule,
  ],
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
  ) {
    iconRegistry.setDefaultFontSetClass('material-symbols-rounded');
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

  isConnectionOpen() {
    return this.channel.getStatus() === ChannelStatus.OPEN;
  }
}

const routes: Routes = [{path: '**', component: Shell}];

@Component({
  selector: 'mesop-app',
  template: '<router-outlet></router-outlet>',
  standalone: true,
  imports: [Shell, RouterOutlet],
  providers: [EditorModeService],
})
class MesopApp {}

export function bootstrapApp() {
  bootstrapApplication(MesopApp, {
    providers: [provideAnimations(), provideRouter(routes)],
  });
}
