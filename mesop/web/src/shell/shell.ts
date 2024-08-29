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
  QueryParam,
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
import {getQueryParams} from '../utils/query_params';
import {
  ErrorDialogService,
  ProdErrorDialogService,
} from '../services/error_dialog_service';
// Keep the following comment to ensure there's a hook for adding TS imports in the downstream sync.
// ADD_TS_IMPORT_HERE

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
    initRequest.setQueryParamsList(getQueryParams());
    request.setInit(initRequest);
    this.channel.init(
      {
        zone: this.zone,
        onRender: async (rootComponent, componentConfigs, jsModules) => {
          // Make sure we clear the error *before* the async work, otherwise
          // we can hit a weird race condition where the error is cleared
          // right away before the user sees the error box.
          this.error = undefined;

          // Import all JS modules concurrently
          await Promise.all(
            jsModules.map((modulePath) =>
              import(modulePath).then(() =>
                console.debug(`Successfully imported JS module: ${modulePath}`),
              ),
            ),
          ).then(() => {
            console.debug('All JS modules imported');
          });
          this.rootComponent = rootComponent;
          // Component configs are only sent for the first response.
          // For subsequent reponses, use the component configs previously
          if (componentConfigs.length) {
            this.componentConfigs = componentConfigs;
          }
        },
        onCommand: (command) => {
          if (command.hasNavigate()) {
            const url = command.getNavigate()!.getUrl()!;
            if (url.startsWith('http://') || url.startsWith('https://')) {
              window.location.href = url;
            } else {
              this.router.navigateByUrl(command.getNavigate()!.getUrl()!);
            }
          } else if (command.hasScrollIntoView()) {
            // Scroll into view
            const key = command.getScrollIntoView()!.getKey();
            // Schedule scroll into view to run after the current event loop tick
            // so that the component has time to render.
            setTimeout(() => {
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
            }, 0);
          } else if (command.hasFocusComponent()) {
            // Focus on component
            const key = command.getFocusComponent()!.getKey();
            const targetElements = document.querySelectorAll(
              `[data-key="${key}"]`,
            );
            if (!targetElements.length) {
              console.error(
                `Could not focus on component with key ${key} because no component found`,
              );
              return;
            }
            if (targetElements.length > 1) {
              console.warn(
                'Found multiple components',
                targetElements,
                'to potentially focus on for key',
                key,
                '. This is probably a bug and you should use a unique key identifier.',
              );
            }
            const matchingElements = targetElements[0].nextElementSibling
              ?.querySelectorAll(`
                a[href]:not([tabindex='-1']),
                area[href]:not([tabindex='-1']),
                input:not([disabled]):not([tabindex='-1']):not([type='file']),
                select:not([disabled]):not([tabindex='-1']),
                textarea:not([disabled]):not([tabindex='-1']),
                button:not([disabled]):not([tabindex='-1']),
                iframe:not([tabindex='-1']),
                [tabindex]:not([tabindex='-1']),
                [contentEditable=true]:not([tabindex='-1'])
              `);
            if (
              matchingElements &&
              typeof matchingElements[0] === 'object' &&
              'focus' in matchingElements[0]
            ) {
              (
                matchingElements[0] as {
                  focus: () => void;
                }
              ).focus();
            } else {
              console.warn(
                `Component with key ${key} does not have a focus method.`,
              );
            }
          } else if (command.hasSetThemeMode()) {
            const themeMode = command.getSetThemeMode();
            if (themeMode?.getThemeMode() == null) {
              throw new Error('Theme mode undefined in setThemeMode command');
            }
            this.themeService.setThemeMode(themeMode);
          } else if (command.hasSetThemeDensity()) {
            const setThemeDensity = command.getSetThemeDensity()!;
            const density = setThemeDensity.getDensity();
            if (density == null) {
              throw new Error('Density undefined in setThemeDensity command');
            }
            this.themeService.setDensity(density);
          } else if (command.hasUpdateQueryParam()) {
            updateUrlFromQueryParam(
              command.getUpdateQueryParam()!.getQueryParam()!,
            );
          } else {
            throw new Error(
              `Unhandled command: ${command.getCommandCase().toString()}`,
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
    providers: [
      provideAnimations(),
      provideRouter(routes),
      EditorService,
      {provide: ErrorDialogService, useClass: ProdErrorDialogService},
    ],
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

function updateUrlFromQueryParam(queryParam: QueryParam) {
  const key = queryParam.getKey()!;
  const values = queryParam.getValuesList();
  const url = new URL(window.location.href);
  url.searchParams.delete(key);

  for (const value of values) {
    url.searchParams.append(key, value);
  }

  window.history.replaceState({}, '', url.toString());
}
