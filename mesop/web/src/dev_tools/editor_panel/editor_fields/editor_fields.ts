import {Component, Input} from '@angular/core';
import {EditorService} from '../../../services/editor_service';
import {mapComponentToObject} from '../../services/logger';
import {mapComponentObjectToDisplay} from '../../component_tree/component_tree';
import {ObjectTree} from '../../object_tree/object_tree';
import {
  FieldType,
  EditorField,
  EditorEvent,
  EditorUpdateCallsite,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatDividerModule} from '@angular/material/divider';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatSelectModule} from '@angular/material/select';
import {CommonModule} from '@angular/common';
import {Channel} from '../../../services/channel';

@Component({
  selector: 'mesop-editor-fields',
  templateUrl: 'editor_fields.ng.html',
  styleUrl: 'editor_fields.css',
  standalone: true,
  imports: [
    ObjectTree,
    MatFormFieldModule,
    MatInputModule,
    MatDividerModule,
    MatCheckboxModule,
    MatSelectModule,
    CommonModule,
  ],
})
export class EditorFields {
  @Input()
  fields!: EditorField[];

  FieldTypeCase = FieldType.TypeCase;

  constructor(
    private editorService: EditorService,
    private channel: Channel,
  ) {}

  onBlur(event: FocusEvent) {
    const target = event.target as HTMLInputElement;
    const editorEvent = new EditorEvent();
    const editorUpdate = new EditorUpdateCallsite();
    editorEvent.setUpdateCallsite(editorUpdate);
    editorUpdate.setSourceCodeLocation(
      this.editorService.getFocusedComponent().getSourceCodeLocation(),
    );
    const name = target.getAttribute('data-name');
    if (!name) {
      throw new Error('Expected to get data-name attribute from event.');
    }
    editorUpdate.setKeywordArgument(name);
    editorUpdate.setNewCode(target.value);
    this.channel.dispatchEditorEvent(editorEvent);
  }

  getFocusedComponent() {
    const obj = mapComponentToObject(this.editorService.getFocusedComponent());
    const display = mapComponentObjectToDisplay(obj);
    return display;
  }

  getFieldsForListField(field: EditorField): EditorField[] {
    return (
      field
        .getType()!
        .getListType()!
        .getType()!
        .getStructType()!
        .getFieldsList() ?? []
    );
  }

  getRegularFields(): EditorField[] {
    return (
      this.fields.filter(
        (field) =>
          field.getType()?.getTypeCase() !== this.FieldTypeCase.BOOL_TYPE &&
          field.getType(),
      ) ?? []
    );
  }

  getBoolFields(): EditorField[] {
    return (
      this.fields.filter(
        (field) =>
          field.getType()?.getTypeCase() === this.FieldTypeCase.BOOL_TYPE,
      ) ?? []
    );
  }

  getNonTypedFields(): EditorField[] {
    return this.fields.filter((field) => !field.getType()) ?? [];
  }

  getValueFor(fieldName: string) {
    return (
      this.getFocusedComponent().properties['value' as any][fieldName as any] ??
      ''
    );
  }
}
