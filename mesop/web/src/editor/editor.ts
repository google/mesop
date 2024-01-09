import {
  Component,
  ElementRef,
  ErrorHandler,
  Injectable,
  NgZone,
  Renderer2,
  ViewChild,
} from '@angular/core';
import {Router, RouterOutlet, Routes, provideRouter} from '@angular/router';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {
  ServerError,
  Component as ComponentProto,
  ComponentConfig,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CommonModule} from '@angular/common';
import {ComponentRenderer} from '../component_renderer/component_renderer';
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
import {Shell} from '../shell/shell';
import {EditorService} from '../services/editor_service';
// Keep the following comment to ensure there's a hook for adding TS imports in the downstream sync.
// ADD_TS_IMPORT_HERE

@Component({
  selector: 'mesop-editor',
  templateUrl: 'editor.ng.html',
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
    Shell,
  ],
  providers: [
    {provide: ErrorHandler, useClass: GlobalErrorHandlerService},
    {provide: HotReloadWatcher, useClass: IbazelHotReloadWatcher},
  ],
  styleUrl: 'editor.css',
})
class Editor {
  rootComponent!: ComponentProto;

  @ViewChild('dragHandle', {read: ElementRef}) dragHandle!: ElementRef;
  private isDragging = false;
  @ViewChild('sidenav', {read: ElementRef}) sidenav!: ElementRef;
  @ViewChild('sidenavContent', {read: ElementRef})
  sidenavContent!: ElementRef;
  @ViewChild(Shell, {static: false}) shell?: Shell;

  constructor(
    private zone: NgZone,
    private renderer: Renderer2,
    // Injecting to ensure it's loaded in the app
    private hotReloadWatcher: HotReloadWatcher,
    // private channel: Channel,
    private devToolsSettings: DevToolsSettings,
    iconRegistry: MatIconRegistry,
    private router: Router,
    errorHandler: ErrorHandler,
    private editorService: EditorService,
  ) {
    iconRegistry.setDefaultFontSetClass('material-symbols-rounded');
    (errorHandler as GlobalErrorHandlerService).setOnError((error) => {
      const errorProto = new ServerError();
      errorProto.setException(`JS Error: ${error.toString()}`);
      this.errors.push(errorProto);
    });
  }

  get errors(): ServerError[] {
    if (!this.shell) return [];
    return this.shell.errors;
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

  showDebugButton() {
    return this.devToolsSettings.isDebugMode();
  }

  showDevTools() {
    return this.devToolsSettings.showDevTools();
  }

  toggleDevTools() {
    this.devToolsSettings.toggleShowDevTools();
    // If we're collapsing devtools, then clear focused component.
    if (!this.devToolsSettings.showDevTools()) {
      console.log('CLEAR');
      this.editorService.clearFocusedComponent();
    }
  }

  componentConfigs(): ComponentConfig[] {
    if (!this.shell) return [];
    return this.shell.componentConfigs;
  }
}

const routes: Routes = [{path: '**', component: Editor}];

@Injectable()
class EditorServiceImpl implements EditorService {
  constructor(private devToolsSettings: DevToolsSettings) {}

  component = new ComponentProto();
  isEditorMode(): boolean {
    return true;
  }

  setFocusedComponent(component: ComponentProto): void {
    if (!this.devToolsSettings.showDevTools()) {
      // Do not focus component if devtools isn't open.
      return;
    }
    this.component = component;
  }

  getFocusedComponent(): ComponentProto {
    return this.component;
  }

  clearFocusedComponent() {
    this.component = new ComponentProto();
  }
}

@Component({
  selector: 'mesop-editor-app',
  template: '<router-outlet></router-outlet>',
  standalone: true,
  providers: [{provide: EditorService, useClass: EditorServiceImpl}],
  imports: [Editor, RouterOutlet],
})
class MesopEditorApp {}

export function bootstrapApp() {
  bootstrapApplication(MesopEditorApp, {
    providers: [provideAnimations(), provideRouter(routes)],
  });
}

export const TEST_ONLY = {EditorServiceImpl};
