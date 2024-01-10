import {Component, Input} from '@angular/core';
import {EditorService} from '../../services/editor_service';
import {mapComponentToObject} from '../services/logger';
import {mapComponentObjectToDisplay} from '../component_tree/component_tree';
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
  imports: [ObjectTree, EditorFields, MatDividerModule],
})
export class EditorPanel {
  @Input()
  componentConfigs!: ComponentConfig[];

  FieldTypeCase = FieldType.TypeCase;

  constructor(private editorService: EditorService) {}

  hasFocusedComponent(): boolean {
    return Boolean(this.editorService.getFocusedComponent());
  }

  getFocusedComponent() {
    const obj = mapComponentToObject(this.editorService.getFocusedComponent()!);
    const display = mapComponentObjectToDisplay(obj);
    return display;
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
}
