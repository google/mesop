import {Component, Input} from '@angular/core';
import {LogsPanel} from './logs_panel/logs_panel';
import {CommonModule} from '@angular/common';
import {DevToolsSettings, Panel} from './services/dev_tools_settings';
import {EditorPanel} from './editor_panel/editor_panel';
import {ComponentConfig} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MatIconModule} from '@angular/material/icon';
import {EditorService, SelectionMode} from '../services/editor_service';
import {MatTooltipModule} from '@angular/material/tooltip';
import {isMac} from '../utils/platform';
import {Channel} from '../services/channel';

@Component({
  selector: 'mesop-dev-tools',
  templateUrl: 'dev_tools.ng.html',
  styleUrl: 'dev_tools.css',
  standalone: true,
  imports: [
    LogsPanel,
    CommonModule,
    EditorPanel,
    MatIconModule,
    MatTooltipModule,
  ],
})
export class DevTools {
  @Input()
  componentConfigs!: ComponentConfig[];

  Panel = Panel; // Make it accessible by template.

  get selectedPanel(): Panel {
    return this.devToolsSettings.getCurrentDevToolsPanel();
  }

  constructor(
    public devToolsSettings: DevToolsSettings,
    private editorService: EditorService,
    private channel: Channel,
  ) {}

  selectEditorPanel() {
    this.devToolsSettings.setCurrentDevToolsPanel(Panel.Components);
  }

  selectLogsPanel() {
    this.devToolsSettings.setCurrentDevToolsPanel(Panel.Logs);
  }

  isSelectingMode(): boolean {
    return this.editorService.getSelectionMode() === SelectionMode.SELECTING;
  }

  toggleSelectingMode(): void {
    switch (this.editorService.getSelectionMode()) {
      case SelectionMode.DISABLED:
      case SelectionMode.SELECTED:
        this.editorService.setSelectionMode(SelectionMode.SELECTING);
        break;
      case SelectionMode.SELECTING:
        this.editorService.setSelectionMode(SelectionMode.DISABLED);
        break;
    }
  }

  getInspectTooltip(): string {
    if (isMac()) {
      return 'Select component - ⌘ ⇧ E';
    }
    return 'Select component - Ctrl ⇧ E';
  }

  getHotReloadTooltip(): string {
    if (isMac()) {
      return 'Hot reload - ⌘ ⇧ R';
    }
    return 'Hot reload - Ctrl ⇧ R';
  }

  hotReload() {
    this.channel.hotReload();
  }
}
