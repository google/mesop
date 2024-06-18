import {Component, Input, ViewChild} from '@angular/core';
import {EditorService} from '../../../services/editor_service';
import {mapComponentToObject} from '../../services/logger';
import {mapComponentObjectToDisplay} from '../../component_tree/component_tree';
import {ObjectTree} from '../../object_tree/object_tree';
import {
  FieldType,
  EditorField,
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
import {MatIconModule} from '@angular/material/icon';
import {CdkTextareaAutosize, TextFieldModule} from '@angular/cdk/text-field';

const EMPTY_ARRAY: [] = []; // Useful for avoiding excessive change detection.

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
  fields!: readonly EditorField[];

  @Input()
  prefixes: Prefixes = [];

  FieldTypeCase = FieldType.TypeCase;
  hoveredFieldName: string | undefined;
  clearHoveredFieldNameTimeoutId: number | undefined;

  cachedPrefixesForFieldName = new Map<string, Prefixes>();
  cachedPrefixesListForFieldName = new Map<string, Prefixes[]>();

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

  getFocusedComponent() {
    const obj = mapComponentToObject(this.editorService.getFocusedComponent()!);
    const display = mapComponentObjectToDisplay(obj);
    return display;
  }

  getFieldsForListField(field: EditorField): readonly EditorField[] {
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
      return EMPTY_ARRAY;
    }
    const cacheKey = `fieldName=${fieldName}|length=${val.length}`;
    if (this.cachedPrefixesListForFieldName.has(cacheKey)) {
      return this.cachedPrefixesListForFieldName.get(cacheKey)!;
    }
    const prefixes = val.map((_, index) => [
      ...this.getPrefixFor(fieldName),
      index,
    ]);
    this.cachedPrefixesListForFieldName.set(cacheKey, prefixes);
    return prefixes;
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

  getPrefixFor(fieldName: string): Prefixes {
    if (this.cachedPrefixesForFieldName.has(fieldName)) {
      return this.cachedPrefixesForFieldName.get(fieldName)!;
    }

    const prefixes = [...this.prefixes, fieldName];
    this.cachedPrefixesForFieldName.set(fieldName, prefixes);
    return prefixes;
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
