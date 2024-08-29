import {
  Component,
  ElementRef,
  HostListener,
  Injectable,
  NgZone,
  Renderer2,
  ViewChild,
} from '@angular/core';
import {Router, RouterOutlet, Routes, provideRouter} from '@angular/router';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {
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
  DefaultHotReloadWatcher,
} from '../services/hot_reload_watcher';
import {Shell, registerComponentRendererElement} from '../shell/shell';
import {EditorService, SelectionMode} from '../services/editor_service';
import {Channel} from '../services/channel';
import {EditorToolbar} from '../editor_toolbar/editor_toolbar';
import {isMac} from '../utils/platform';
import {
  DebugErrorDialogService,
  ErrorDialogService,
} from '../services/error_dialog_service';
import {ExperimentService} from '../services/experiment_service';
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
    EditorToolbar,
    ErrorBox,
    DevTools,
    MatIconModule,
    MatButtonModule,
    MatSidenavModule,
    Shell,
  ],
  providers: [{provide: HotReloadWatcher, useClass: DefaultHotReloadWatcher}],
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
    private hostElement: ElementRef,
    private zone: NgZone,
    private renderer: Renderer2,
    // Injecting to ensure it's loaded in the app
    private hotReloadWatcher: HotReloadWatcher,
    // private channel: Channel,
    private devToolsSettings: DevToolsSettings,
    iconRegistry: MatIconRegistry,
    private router: Router,
    private editorService: EditorService,
    private channel: Channel,
    private experimentService: ExperimentService,
  ) {
    iconRegistry.setDefaultFontSetClass('material-symbols-rounded');
    this.renderer.setAttribute(
      this.hostElement.nativeElement,
      'tabindex',
      '-1',
    );
  }

  ngAfterViewInit() {
    this.hostElement.nativeElement.focus();

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

  showDevTools() {
    return this.devToolsSettings.showDevTools();
  }

  toggleDevTools() {
    this.devToolsSettings.toggleShowDevTools();
    // If we're collapsing devtools, then clear focused component.
    if (!this.devToolsSettings.showDevTools()) {
      this.editorService.clearFocusedComponent();
    }
  }

  componentConfigs(): readonly ComponentConfig[] {
    if (!this.shell) return [];
    return this.shell.componentConfigs;
  }

  @HostListener('window:keydown', ['$event'])
  handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      this.editorService.clearFocusedComponent();
      return;
    }
    // Hotkey for toggle selection mode
    //
    // Binds:
    // cmd + shift + e (MacOs)
    // ctrl + shift + e (Other platforms)
    if (
      event.key === 'e' &&
      (isMac() ? event.metaKey : event.ctrlKey) &&
      event.shiftKey
    ) {
      this.editorService.toggleSelectionMode();
      event.preventDefault();
      return;
    }
    // Hotkey for hot reload
    //
    // Binds:
    // cmd + shift + r (MacOs)
    // ctrl + shift + r (Other platforms)
    if (
      event.key === 'r' &&
      (isMac() ? event.metaKey : event.ctrlKey) &&
      event.shiftKey
    ) {
      this.channel.hotReload();
      event.preventDefault();
      return;
    }
  }

  showEditorToolbar(): boolean {
    return this.experimentService.experimentalEditorToolbarEnabled;
  }
}

const routes: Routes = [{path: '**', component: Editor}];

@Injectable()
class EditorServiceImpl implements EditorService {
  selectionMode: SelectionMode = SelectionMode.DISABLED;
  onSelectedComponent: ((component: ComponentProto) => void) | undefined;
  constructor(
    private channel: Channel,
    private devToolsSettings: DevToolsSettings,
  ) {}

  indexPath: number[] | undefined;
  isEditorMode(): boolean {
    return true;
  }

  getSelectionMode(): SelectionMode {
    return this.selectionMode;
  }

  setSelectionMode(mode: SelectionMode): void {
    this.selectionMode = mode;
    if (mode === SelectionMode.SELECTED) {
      this.onSelectedComponent?.(this.getFocusedComponent()!);
    }
  }

  setOnSelectedComponent(callback: (component: ComponentProto) => void) {
    this.onSelectedComponent = callback;
  }

  toggleSelectionMode(): void {
    switch (this.selectionMode) {
      case SelectionMode.DISABLED:
      case SelectionMode.SELECTED:
        this.selectionMode = SelectionMode.SELECTING;
        break;
      case SelectionMode.SELECTING:
        this.selectionMode = SelectionMode.DISABLED;
        break;
    }
  }

  setFocusedComponent(component: ComponentProto): void {
    const root = this.channel.getRootComponent();
    if (!root) {
      throw new Error('No root component');
    }
    const indexPath: number[] = [];
    if (!findPath(root, component, indexPath)) {
      console.error('Did not find component path for', component);
    }
    this.indexPath = indexPath;
  }

  getFocusedComponent(): ComponentProto | undefined {
    if (!this.indexPath) {
      return;
    }
    let node = this.channel.getRootComponent();
    if (!node) {
      throw new Error('No root component');
    }
    for (const index of this.indexPath) {
      node = node.getChildrenList()[index];
      if (!node) {
        return;
      }
    }
    return node;
  }

  clearFocusedComponent() {
    this.indexPath = undefined;
  }
}

function findPath(
  root: ComponentProto,
  target: ComponentProto,
  indexPath: number[],
): boolean {
  if (root === target) return true;
  for (let i = 0; i < root.getChildrenList().length; i++) {
    indexPath.push(i);
    if (findPath(root.getChildrenList()[i], target, indexPath)) {
      return true;
    }
    indexPath.pop();
  }
  return false;
}

@Component({
  selector: 'mesop-editor-app',
  template: '<router-outlet></router-outlet>',
  imports: [Editor, RouterOutlet],
  standalone: true,
})
class MesopEditorApp {}

export async function bootstrapApp() {
  const app = await bootstrapApplication(MesopEditorApp, {
    providers: [
      provideAnimations(),
      provideRouter(routes),
      {provide: EditorService, useClass: EditorServiceImpl},
      {provide: ErrorDialogService, useClass: DebugErrorDialogService},
    ],
  });
  registerComponentRendererElement(app);
}

export const TEST_ONLY = {EditorServiceImpl};
