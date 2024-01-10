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
  ArgPath,
  ArgPathSegment,
  CodeValue,
  LiteralElement,
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

  @Input()
  prefixes: string[] = [];

  FieldTypeCase = FieldType.TypeCase;

  constructor(
    private editorService: EditorService,
    private channel: Channel,
  ) {}

  onNewProperty(event: Event) {
    const target = event.target as HTMLSelectElement;
    const editorEvent = new EditorEvent();
    const editorUpdate = new EditorUpdateCallsite();
    editorEvent.setUpdateCallsite(editorUpdate);
    editorUpdate.setSourceCodeLocation(
      this.editorService.getFocusedComponent()!.getSourceCodeLocation(),
    );
    editorUpdate.setComponentName(
      this.editorService.getFocusedComponent()!.getType()!.getName(),
    );
    const argPath = new ArgPath();
    for (const prefix of this.prefixes) {
      const segment = new ArgPathSegment();
      segment.setKeywordArgument(prefix);
      argPath.addSegments(segment);
    }
    const segment = new ArgPathSegment();
    segment.setKeywordArgument(target.value);
    argPath.addSegments(segment);
    editorUpdate.setArgPath(argPath);

    const type = this.fields
      .find((f) => f.getName() === target.value)!
      .getType();
    const newCode = new CodeValue();
    switch (type?.getTypeCase()) {
      case FieldType.TypeCase.STRUCT_TYPE:
        newCode.setStructName(type.getStructType()!.getStructName());
        break;
      case FieldType.TypeCase.STRING_TYPE:
        newCode.setStringValue('<new>');
        break;
      default:
        throw new Error(`Unhandled case: ${type?.getTypeCase()}`);
    }
    editorUpdate.setNewCode(newCode);
    this.channel.dispatchEditorEvent(editorEvent);
  }

  onBlur(event: FocusEvent) {
    const target = event.target as HTMLInputElement;
    const editorEvent = new EditorEvent();
    const editorUpdate = new EditorUpdateCallsite();
    editorEvent.setUpdateCallsite(editorUpdate);
    editorUpdate.setSourceCodeLocation(
      this.editorService.getFocusedComponent()!.getSourceCodeLocation(),
    );
    const name = target.getAttribute('data-name');
    if (!name) {
      throw new Error('Expected to get data-name attribute from event.');
    }
    editorUpdate.setComponentName(
      this.editorService.getFocusedComponent()!.getType()!.getName(),
    );
    const argPath = new ArgPath();
    for (const prefix of this.prefixes) {
      const segment = new ArgPathSegment();
      segment.setKeywordArgument(prefix);
      argPath.addSegments(segment);
    }
    const segment = new ArgPathSegment();
    segment.setKeywordArgument(name);
    argPath.addSegments(segment);
    editorUpdate.setArgPath(argPath);
    const codeValue = new CodeValue();
    codeValue.setStringValue(target.value);
    editorUpdate.setNewCode(codeValue);
    this.channel.dispatchEditorEvent(editorEvent);
  }

  getFocusedComponent() {
    const obj = mapComponentToObject(this.editorService.getFocusedComponent()!);
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
          field.getType() &&
          this.getValueFor(field.getName()),
      ) ?? []
    );
  }

  getHiddenFields() {
    return (
      this.fields
        .filter(
          (field) =>
            field.getType()?.getTypeCase() !== this.FieldTypeCase.BOOL_TYPE &&
            field.getType() &&
            !this.getValueFor(field.getName()),
        )
        .map((field) => field.getName()) ?? []
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

  getPrefixFor(fieldName: string) {
    return [...this.prefixes, fieldName];
  }

  getValueFor(fieldName: string) {
    let valueObj = this.getFocusedComponent().properties['value' as any];
    for (const prefix of this.prefixes) {
      valueObj = valueObj[prefix as any];
      if (!valueObj) {
        return '';
      }
    }
    const value = valueObj[fieldName as any] ?? '';
    return value;
  }

  getLiteralValue(literal: LiteralElement): string {
    switch (literal.getLiteralCase()) {
      case LiteralElement.LiteralCase.INT_LITERAL:
        return literal.getIntLiteral().toString();
      case LiteralElement.LiteralCase.STRING_LITERAL:
        return literal.getStringLiteral();
      case LiteralElement.LiteralCase.LITERAL_NOT_SET:
        throw new Error(`Unhandled literal element case ${literal.toObject()}`);
    }
  }
}
