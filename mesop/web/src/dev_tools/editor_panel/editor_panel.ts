import {Component, Input} from '@angular/core';
import {EditorService} from '../../services/editor_service';
import {ComponentObject, Logger, RenderLogModel} from '../services/logger';
import {ComponentTree, FlatNode} from '../component_tree/component_tree';
import {ObjectTree} from '../object_tree/object_tree';
import {
  FieldType,
  ComponentConfig,
  EditorField,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MatDividerModule} from '@angular/material/divider';
import {EditorFields} from './editor_fields/editor_fields';

@Component({
  selector: 'mesop-editor-panel',
  templateUrl: 'editor_panel.ng.html',
  styleUrl: 'editor_panel.css',
  standalone: true,
  imports: [ObjectTree, EditorFields, MatDividerModule, ComponentTree],
})
export class EditorPanel {
  @Input()
  componentConfigs!: ComponentConfig[];

  FieldTypeCase = FieldType.TypeCase;
  selectedNode!: FlatNode;

  constructor(
    private logger: Logger,
    private editorService: EditorService,
  ) {}

  hasFocusedComponent(): boolean {
    return Boolean(this.editorService.getFocusedComponent());
  }

  getFocusedComponent() {
    return this.editorService.getFocusedComponent();
  }

  getComponentConfig() {
    return this.componentConfigs.find(
      (config) =>
        config.getComponentName() ===
        this.editorService.getFocusedComponent()!.getType()?.getName(),
    );
  }

  getFields(): EditorField[] {
    return this.getComponentConfig()?.getFieldsList() ?? [];
  }

  component(): ComponentObject {
    const renderLog = this.logger
      .getLogs()
      .slice()
      .reverse()
      .find((log) => log.type === 'Render') as RenderLogModel;
    return renderLog?.rootComponent as ComponentObject;
  }
}
