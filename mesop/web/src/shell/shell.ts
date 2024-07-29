import {
  ApplicationRef,
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
  ResizeEvent,
  UiRequest,
  InitRequest,
  ThemeMode,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CommonModule} from '@angular/common';
import {
  COMPONENT_RENDERER_ELEMENT_NAME,
  ComponentRenderer,
} from '../component_renderer/component_renderer';
import {Channel} from '../services/channel';
import {provideAnimations} from '@angular/platform-browser/animations';
import {bootstrapApplication} from '@angular/platform-browser';
import {MatIconModule, MatIconRegistry} from '@angular/material/icon';
import {EditorService} from '../services/editor_service';
import {MatSidenavModule} from '@angular/material/sidenav';
import {ErrorBox} from '../error/error_box';
import {GlobalErrorHandlerService} from '../services/global_error_handler';
import {getViewportSize} from '../utils/viewport_size';
import {createCustomElement} from '@angular/elements';
import {Subject} from 'rxjs';
import {debounceTime} from 'rxjs/operators';
import {ThemeService} from '../services/theme_service';

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
  error: ServerError | undefined;
  componentConfigs: readonly ComponentConfig[] = [];
  private resizeSubject = new Subject<void>();

  constructor(
    private zone: NgZone,
    private renderer: Renderer2,
    private channel: Channel,
    iconRegistry: MatIconRegistry,
    private router: Router,
    errorHandler: ErrorHandler,
    private themeService: ThemeService,
  ) {
    iconRegistry.setDefaultFontSetClass('material-symbols-rounded');
    (errorHandler as GlobalErrorHandlerService).setOnError((error) => {
      const errorProto = new ServerError();
      errorProto.setException(`JS Error: ${error.toString()}`);
      this.error = errorProto;
    });
    this.resizeSubject
      .pipe(debounceTime(500))
      .subscribe(() => this.onResizeDebounced());
  }

  ngOnInit() {
    const request = new UiRequest();
    const initRequest = new InitRequest();
    initRequest.setViewportSize(getViewportSize());
    initRequest.setThemeSettings(this.themeService.getThemeSettings());
    request.setInit(initRequest);
    this.channel.init(
      {
        zone: this.zone,
        onRender: (rootComponent, componentConfigs) => {
          this.rootComponent = rootComponent;
          // Component configs are only sent for the first response.
          // For subsequent reponses, use the component configs previously
          if (componentConfigs.length) {
            this.componentConfigs = componentConfigs;
          }
          this.error = undefined;
        },
        onCommand: (command) => {
          if (command.hasNavigate()) {
            this.router.navigateByUrl(command.getNavigate()!.getUrl()!);
          } else if (command.hasScrollIntoView()) {
            // Scroll into view
            const key = command.getScrollIntoView()!.getKey();
            const targetElements = document.querySelectorAll(
              `[data-key="${key}"]`,
            );
            if (!targetElements.length) {
              console.error(
                `Could not scroll to component with key ${key} because no component found`,
              );
              return;
            }
            if (targetElements.length > 1) {
              console.warn(
                'Found multiple components',
                targetElements,
                'to potentially scroll to for key',
                key,
                '. This is probably a bug and you should use a unique key identifier.',
              );
            }
            targetElements[0].parentElement!.scrollIntoView({
              behavior: 'smooth',
            });
          } else if (command.hasSetThemeMode()) {
            const themeMode = command.getSetThemeMode();
            if (themeMode?.getThemeMode() == null) {
              throw new Error('Theme mode undefined in setThemeMode command');
            }
            this.themeService.setThemeMode(themeMode);
          } else {
            throw new Error(
              'Unhandled command: ' + command.getCommandCase().toString(),
            );
          }
        },
        onError: (error) => {
          this.error = error;
        },
      },
      request,
    );
  }

  /** Listen to browser navigation events (go back/forward). */
  @HostListener('window:popstate', ['$event'])
  onPopState(event: Event) {
    const userEvent = new UserEvent();
    userEvent.setNavigation(new NavigationEvent());
    this.channel.dispatch(userEvent);
  }

  showChannelProgressIndicator(): boolean {
    return this.channel.isBusy();
  }

  @HostListener('window:resize')
  onResize(event: Event) {
    this.resizeSubject.next();
  }

  onResizeDebounced() {
    const userEvent = new UserEvent();
    userEvent.setResize(new ResizeEvent());
    this.channel.dispatch(userEvent);
  }
}

const routes: Routes = [{path: '**', component: Shell}];

@Component({
  selector: 'mesop-app',
  template: '<router-outlet></router-outlet>',
  imports: [Shell, RouterOutlet],
  standalone: true,
})
class MesopApp {}

export async function bootstrapApp() {
  const app = await bootstrapApplication(MesopApp, {
    providers: [provideAnimations(), provideRouter(routes), EditorService],
  });
  registerComponentRendererElement(app);
}

export function registerComponentRendererElement(app: ApplicationRef) {
  const ComponentRendererElement = createCustomElement(ComponentRenderer, {
    injector: app.injector,
  });
  customElements.define(
    COMPONENT_RENDERER_ELEMENT_NAME,
    ComponentRendererElement,
  );
}
