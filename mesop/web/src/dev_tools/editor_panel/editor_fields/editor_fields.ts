import {Component, Input, ViewChild} from '@angular/core';
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
  CodeReplacement,
  DeleteCode,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatDividerModule} from '@angular/material/divider';
import {MatCheckboxChange, MatCheckboxModule} from '@angular/material/checkbox';
import {MatSelectModule} from '@angular/material/select';
import {CommonModule} from '@angular/common';
import {Channel} from '../../../services/channel';
import {MatIconModule} from '@angular/material/icon';
import {CdkTextareaAutosize, TextFieldModule} from '@angular/cdk/text-field';

// string is field name; number is list index
type Prefix = string | number;
type Prefixes = Prefix[];

@Component({
  selector: 'mesop-editor-fields',
  templateUrl: 'editor_fields.ng.html',
  styleUrl: 'editor_fields.css',
  standalone: true,
  imports: [
    ObjectTree,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatDividerModule,
    MatCheckboxModule,
    MatSelectModule,
    TextFieldModule,
    CommonModule,
  ],
})
export class EditorFields {
  @Input()
  fields!: EditorField[];

  @Input()
  prefixes: Prefixes = [];

  FieldTypeCase = FieldType.TypeCase;
  hoveredFieldName: string | undefined;
  clearHoveredFieldNameTimeoutId: number | undefined;

  @ViewChild('autosize') autosize: CdkTextareaAutosize | undefined;

  constructor(
    private editorService: EditorService,
    private channel: Channel,
  ) {}

  ngOnChanges() {
    // Hack to force textarea to resize.
    setTimeout(() => {
      if (this.autosize) {
        this.autosize.resizeToFitContent(true);
      }
    }, 0);
  }

  onMouseenter(fieldName: string): void {
    this.hoveredFieldName = fieldName;
    clearTimeout(this.clearHoveredFieldNameTimeoutId);
    this.clearHoveredFieldNameTimeoutId = setTimeout(() => {
      this.hoveredFieldName = undefined;
    }, 3000);
  }

  clearHoveredFieldName(): void {
    this.hoveredFieldName = undefined;
  }

  onNewProperty(event: Event) {
    const target = event.target as HTMLSelectElement;

    const segment = new ArgPathSegment();
    segment.setKeywordArgument(target.value);
    const type = this.fields
      .find((f) => f.getName() === target.value)!
      .getType()!;
    this.editWithNewCode(segment, getCodeFromType(type));

    // Reset to the first option (empty) to avoid cutoff text
    target.selectedIndex = 0;
  }

  onSelectLiteral(event: Event) {
    const target = event.target as HTMLSelectElement;
    const segment = new ArgPathSegment();
    const name = target.getAttribute('data-name');
    if (!name) {
      throw new Error('Expected to get data-name attribute from event.');
    }
    segment.setKeywordArgument(name);

    const literalIndex = Number(target.value);
    const literal = this.fields
      .find((f) => f.getName() === name)!
      .getType()!
      .getLiteralType()!
      .getLiteralsList()[literalIndex];

    this.editWithNewCode(segment, getLiteralCodeValue(literal));
  }

  onCheckboxChange(event: MatCheckboxChange) {
    const target = event.source;
    const segment = new ArgPathSegment();
    const name = target.value;
    if (!name) {
      throw new Error('Expected to get name.');
    }
    segment.setKeywordArgument(name);

    const codeValue = new CodeValue();
    codeValue.setBoolValue(event.checked);
    this.editWithNewCode(segment, codeValue);
  }

  onBlur(event: FocusEvent) {
    const target = event.target as HTMLInputElement;
    const segment = new ArgPathSegment();
    const name = target.getAttribute('data-name');
    if (!name) {
      throw new Error('Expected to get data-name attribute from event.');
    }
    segment.setKeywordArgument(name);
    const codeValue = new CodeValue();
    codeValue.setStringValue(target.value);
    this.editWithNewCode(segment, codeValue);
  }

  deleteField(fieldName: string) {
    const segment = new ArgPathSegment();
    segment.setKeywordArgument(fieldName);
    const replacement = new CodeReplacement();
    replacement.setDeleteCode(new DeleteCode());
    this.dispatchEdit([segment], replacement);
  }

  deleteFieldWithIndex(fieldName: string, index: number) {
    const segment1 = new ArgPathSegment();
    segment1.setKeywordArgument(fieldName);
    const segment2 = new ArgPathSegment();
    segment2.setListIndex(index);

    const replacement = new CodeReplacement();
    replacement.setDeleteCode(new DeleteCode());
    this.dispatchEdit([segment1, segment2], replacement);
  }

  appendListElement(fieldName: string) {
    const segment1 = new ArgPathSegment();
    segment1.setKeywordArgument(fieldName);

    const segment2 = new ArgPathSegment();
    const index = this.getPrefixesListForListField(fieldName).length - 1;
    segment2.setListIndex(index);

    const type = this.fields.find((f) => f.getName() === fieldName)!.getType()!;
    const replacement = new CodeReplacement();
    replacement.setAppendElement(getCodeFromType(type));
    this.dispatchEdit([segment1, segment2], replacement);
  }

  private editWithNewCode(
    argPathSegment: ArgPathSegment,
    codeValue: CodeValue,
  ) {
    const replacement = new CodeReplacement();
    replacement.setNewCode(codeValue);
    this.dispatchEdit([argPathSegment], replacement);
  }

  private dispatchEdit(
    argPathSegments: ArgPathSegment[],
    replacement: CodeReplacement,
  ) {
    const editorEvent = new EditorEvent();
    const editorUpdate = new EditorUpdateCallsite();
    editorEvent.setUpdateCallsite(editorUpdate);
    editorUpdate.setSourceCodeLocation(
      this.editorService.getFocusedComponent()!.getSourceCodeLocation(),
    );
    editorUpdate.setComponentName(
      this.editorService.getFocusedComponent()!.getType()!.getName()!,
    );
    const argPath = new ArgPath();
    for (const prefix of this.prefixes) {
      const segment = new ArgPathSegment();
      if (typeof prefix === 'string') {
        segment.setKeywordArgument(prefix);
      } else {
        segment.setListIndex(prefix);
      }
      argPath.addSegments(segment);
    }
    for (const segment of argPathSegments) {
      argPath.addSegments(segment);
    }
    editorUpdate.setArgPath(argPath);
    editorUpdate.setReplacement(replacement);
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

  getPrefixesListForListField(fieldName: string): Prefixes[] {
    const val = this.getValueFor(fieldName) as any[];
    if (!val) {
      return [];
    }
    return val.map((_, index) => [...this.getPrefixFor(fieldName), index]);
  }

  getRegularFields(): EditorField[] {
    return (
      this.fields.filter(
        (field) =>
          field.getType()?.getTypeCase() !== this.FieldTypeCase.BOOL_TYPE &&
          field.getType() &&
          this.getValueFor(field.getName()!) != null,
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
            !this.getValueFor(field.getName()!),
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
    if (fieldName === 'key') {
      return this.getFocusedComponent().properties['key' as any];
    }
    let valueObj = this.getFocusedComponent().properties['value' as any];
    for (const prefix of this.prefixes) {
      valueObj = valueObj[prefix as any];
      if (!valueObj) {
        return undefined;
      }
    }
    const value = valueObj[fieldName as any] ?? undefined;
    return value;
  }

  isLiteralSelected(fieldName: string, literal: LiteralElement): boolean {
    // Doing a toString because getLiteralValue also does a toString() for display purposes.
    return (
      this.getValueFor(fieldName).toString() === this.getLiteralValue(literal)
    );
  }

  getLiteralValue(literal: LiteralElement): string {
    switch (literal.getLiteralCase()) {
      case LiteralElement.LiteralCase.INT_LITERAL:
        return literal.getIntLiteral()!.toString();
      case LiteralElement.LiteralCase.STRING_LITERAL:
        return literal.getStringLiteral()!;
      case LiteralElement.LiteralCase.LITERAL_NOT_SET:
        throw new Error(`Unhandled literal element case ${literal.toObject()}`);
    }
  }
}
function getCodeFromType(type: FieldType): CodeValue {
  const newCode = new CodeValue();
  switch (type!.getTypeCase()) {
    case FieldType.TypeCase.STRUCT_TYPE:
      newCode.setStructName(type.getStructType()!.getStructName()!);
      return newCode;
    case FieldType.TypeCase.STRING_TYPE:
      newCode.setStringValue(type.getStringType()!.getDefaultValue()!);
      return newCode;
    case FieldType.TypeCase.BOOL_TYPE:
      newCode.setBoolValue(type.getBoolType()!.getDefaultValue()!);
      return newCode;
    case FieldType.TypeCase.INT_TYPE:
      newCode.setIntValue(type.getIntType()!.getDefaultValue()!);
      return newCode;
    case FieldType.TypeCase.FLOAT_TYPE:
      newCode.setDoubleValue(type.getFloatType()!.getDefaultValue()!);
      return newCode;
    case FieldType.TypeCase.LITERAL_TYPE: {
      const defaultLiteral = type.getLiteralType()!.getLiteralsList()[0];
      return getLiteralCodeValue(defaultLiteral);
    }
    case FieldType.TypeCase.LIST_TYPE:
      newCode.setStructName(
        type.getListType()!.getType()!.getStructType()!.getStructName()!,
      );
      return newCode;
    case FieldType.TypeCase.TYPE_NOT_SET:
      throw new Error('Unexpected type not set');
  }
}
function getLiteralCodeValue(defaultLiteral: LiteralElement): CodeValue {
  const newCode = new CodeValue();
  switch (defaultLiteral.getLiteralCase()) {
    case LiteralElement.LiteralCase.INT_LITERAL:
      newCode.setIntValue(defaultLiteral.getIntLiteral()!);
      return newCode;
    case LiteralElement.LiteralCase.STRING_LITERAL:
      newCode.setStringValue(defaultLiteral.getStringLiteral()!);
      return newCode;
    case LiteralElement.LiteralCase.LITERAL_NOT_SET:
      throw new Error('Unexpected unset literal case');
  }
}
