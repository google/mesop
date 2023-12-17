import ts from 'typescript';
// @ts-ignore
import fs from 'fs';
// @ts-ignore
import path from 'path';

import * as pb from './component_spec_jspb_proto_pb/generator/component_spec_pb';
import {
  assert,
  capitalize,
  kebabCase,
  parseArgs,
  upperCamelCase,
} from './utils';

const checkboxSpecInput = new pb.ComponentSpecInput();
checkboxSpecInput.setName('checkbox');
checkboxSpecInput.setHasContent(true);

const buttonSpecInput = new pb.ComponentSpecInput();
buttonSpecInput.setName('button');
buttonSpecInput.setElementName('button');
buttonSpecInput.addDirectiveNames('mat-button');
buttonSpecInput.addDirectiveNames('mat-raised-button');
buttonSpecInput.addDirectiveNames('mat-flat-button');
buttonSpecInput.addDirectiveNames('mat-stroked-button');
buttonSpecInput.addNativeEvents('click');
buttonSpecInput.setTsFilename('button-base.ts');
buttonSpecInput.setTargetClass('MatButtonBase'); // Special-case: https://github.com/angular/components/blob/main/src/material/button/button-base.ts
buttonSpecInput.setHasContent(true);
buttonSpecInput.addSkipPropertyNames('disabledInteractive');
buttonSpecInput.addSkipPropertyNames('ariaDisabled'); // not recognized by angular compiler

const inputSpecInput = (() => {
  const i = new pb.ComponentSpecInput();
  i.setName('input');
  i.setElementName('input');
  i.addDirectiveNames('matInput');
  i.addNativeEvents('input');
  i.setIsFormField(true);
  i.addSkipPropertyNames('errorStateMatcher');
  return i;
})();

const formFieldSpecInput = (() => {
  const i = new pb.ComponentSpecInput();
  i.setName('form_field');
  i.setHasContent(true);
  return i;
})();

const tooltipSpecInput = (() => {
  const i = new pb.ComponentSpecInput();
  i.setName('tooltip');
  i.addSkipPropertyNames('tooltipClass');
  i.setHasContent(true);
  return i;
})();

const dividerSpecInput = (() => {
  const i = new pb.ComponentSpecInput();
  i.setName('divider');
  return i;
})();

const badgeSpecInput = (() => {
  const i = new pb.ComponentSpecInput();
  i.setName('badge');
  // Using div as a simple inline container (must be a block-element per https://material.angular.io/components/badge/overview)
  i.setElementName('div');
  i.addDirectiveNames('matBadge');
  i.setHasContent(true);
  return i;
})();

const SYSTEM_IMPORT_PREFIX = '@angular/material/';
const SYSTEM_PREFIX = 'Mat';
const SPEC_INPUTS = [
  tooltipSpecInput,
  inputSpecInput,
  buttonSpecInput,
  checkboxSpecInput,
  formFieldSpecInput,
  badgeSpecInput,
  dividerSpecInput,
].map(preprocessSpecInput);

function preprocessSpecInput(
  input: pb.ComponentSpecInput,
): pb.ComponentSpecInput {
  const name = input.getName();
  if (!input.getTargetClass()) {
    input.setTargetClass(SYSTEM_PREFIX + upperCamelCase(name));
  }
  if (!input.getElementName()) {
    input.setElementName(SYSTEM_PREFIX.toLowerCase() + '-' + kebabCase(name));
  }
  const ngModules = input.getNgModulesList();
  if (!ngModules.length) {
    const ngModule = input.addNgModules();
    ngModule.setModuleName(SYSTEM_PREFIX + upperCamelCase(name) + 'Module');
    ngModule.setImportPath(SYSTEM_IMPORT_PREFIX + kebabCase(name));
  }
  if (input.getIsFormField()) {
    const ngModule = input.addNgModules();
    ngModule.setModuleName(SYSTEM_PREFIX + 'FormFieldModule');
    ngModule.setImportPath(SYSTEM_IMPORT_PREFIX + 'form-field');
  }
  return input;
}

interface Issue {
  msg: string;
  context: any;
  node: any;
}

class NgParser {
  initDefaultMap(): Map<string, pb.XType> {
    const map = new Map<string, pb.XType>();

    // Hard to infer ThemePalette since it's in a central file.
    const xType = new pb.XType();
    const sl = new pb.StringLiterals();
    sl.setStringLiteralList(['primary', 'accent', 'warn']);
    sl.setDefaultValue('primary');
    xType.setStringLiterals(sl);
    map.set('ThemePalette', xType);
    return map;
  }
  proto: pb.ComponentSpec;
  private issues: Issue[] = [];
  private currentNode!: ts.Node;
  sourceFile!: ts.SourceFile;
  private typeAliasMap: Map<string, pb.XType> = this.initDefaultMap();
  constructor(
    private readonly input: pb.ComponentSpecInput,
    filePath: string,
  ) {
    this.proto = new pb.ComponentSpec();
    this.proto.setInput(input);
    this.parseTs(filePath);
  }

  parseTs(filePath: string) {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    this.sourceFile = ts.createSourceFile(
      filePath,
      fileContents,
      ts.ScriptTarget.Latest,
      true, // setParentNodes flag
    );
    for (const statement of this.sourceFile.statements) {
      if (ts.isTypeAliasDeclaration(statement)) {
        this.collectTypeAliases(statement);
      }
    }
    this.sourceFile.statements.find((s) => {
      if (ts.isClassDeclaration(s)) {
        if (s.name?.escapedText === this.input.getTargetClass()) {
          this.processClass(s);
        }
      }
    });
  }
  collectTypeAliases(statement: ts.TypeAliasDeclaration) {
    this.currentNode = statement;
    const name = statement.name.getText();
    if (statement.type) {
      const xType = this.getType(statement.type);
      this.typeAliasMap.set(name, xType);
    }
  }

  logIssue(msg: string, context?: object | string) {
    this.issues.push({msg, context, node: this.currentNode?.getText()});
  }

  validate(): boolean {
    const FgRed = '\x1b[31m';
    const FgGreen = '\x1b[32m';
    const Reset = '\x1b[0m';
    // Filter out skipped property names
    this.proto.setInputPropsList(
      this.proto
        .getInputPropsList()
        .filter(
          (prop) =>
            !this.input.getSkipPropertyNamesList().includes(prop.getName()),
        ),
    );
    this.proto.setOutputPropsList(
      this.proto
        .getOutputPropsList()
        .filter(
          (prop) =>
            !this.input.getSkipPropertyNamesList().includes(prop.getName()),
        ),
    );
    if (this.issues.length) {
      console.error(FgRed, '========================');
      console.error(FgRed, this.issues.length + ' issues found', Reset);
      for (const issue of this.issues) {
        console.error(issue.msg, issue.context, issue.node);
      }
      return false;
    } else {
      console.log(FgGreen, 'Validation succeeded!', Reset);
      return true;
    }
  }

  processClass(cls: ts.ClassDeclaration) {
    for (const member of cls.members) {
      if (ts.isGetAccessor(member) && member.modifiers) {
        for (const modifier of member.modifiers) {
          if (
            ts.isDecorator(modifier) &&
            ts.isCallExpression(modifier.expression) &&
            ts.isIdentifier(modifier.expression.expression)
          ) {
            const identifier = modifier.expression.expression;
            if (identifier.escapedText === 'Input') {
              this.processInputGetAccessor(
                member,
                modifier.expression.arguments,
              );
              continue;
            }
          }
        }

        continue;
      }
      if (!ts.isPropertyDeclaration(member)) {
        continue;
      }
      const prop = member as ts.PropertyDeclaration;
      this.currentNode = prop;
      if (!prop.modifiers) {
        continue;
      }
      for (const modifier of prop.modifiers) {
        if (
          ts.isDecorator(modifier) &&
          ts.isCallExpression(modifier.expression) &&
          ts.isIdentifier(modifier.expression.expression)
        ) {
          const identifier = modifier.expression.expression;
          if (identifier.escapedText === 'Input') {
            this.processInputPropertyDeclaration(
              prop,
              modifier.expression.arguments,
            );
          } else if (identifier.escapedText === 'Output') {
            this.processOutput(prop);
          }
        }
      }
    }
  }

  processInputGetAccessor(
    member: ts.GetAccessorDeclaration,
    args: ts.NodeArray<ts.Expression>,
  ) {
    this.currentNode = member;
    const inputProp = new pb.Prop();
    const name = member.name.getText();
    // Skip properties like errorStateMatcher on input which doesn't have an explicit type.
    if (this.input.getSkipPropertyNamesList().includes(name)) {
      return;
    }
    inputProp.setName(name);
    if (args[0]) {
      inputProp.setAlias(this.getAliasFromInputCallArgument(args));
    }
    if (
      !member.type &&
      name === 'message' &&
      this.input.getName() === 'tooltip'
    ) {
      const type = new pb.XType();
      type.setSimpleType(pb.SimpleType.STRING);
      inputProp.setType(type);
    } else if (!member.type) {
      this.logIssue('no type', {member: member.getText()});
      return;
    } else {
      inputProp.setDebugType(member.type!.getText());
      inputProp.setType(this.getType(assert(member.type)));
    }
    inputProp.setDocs(this.getJsDoc(member));
    this.proto.addInputProps(inputProp);
  }

  processInputPropertyDeclaration(
    prop: ts.PropertyDeclaration,
    args: ts.NodeArray<ts.Expression>,
  ): void {
    this.currentNode = prop;
    const name = prop.name;
    if (ts.isIdentifier(name)) {
      const elName = name.escapedText.toString();
      const inputProp = new pb.Prop();
      if (args[0]) {
        inputProp.setAlias(this.getAliasFromInputCallArgument(args));
      }
      inputProp.setName(elName);
      inputProp.setDebugType(prop.type!.getText());
      inputProp.setType(this.getType(assert(prop.type), prop.initializer));
      inputProp.setDocs(this.getJsDoc(prop));
      this.proto.addInputProps(inputProp);
    } else {
      throw new Error('Expected identifier for prop' + prop);
    }
  }

  private getAliasFromInputCallArgument(
    args: ts.NodeArray<ts.Expression>,
  ): string {
    if (ts.isObjectLiteralExpression(args[0])) {
      const objectLiteral = args[0];
      for (const p of objectLiteral.properties) {
        if (ts.isPropertyAssignment(p) && p.name.getText() === 'alias') {
          return this.stripQuotes(p.initializer.getText());
        }
      }
      // Sometimes there's no alias.
      return '';
    }
    return this.stripQuotes(args[0].getText());
  }

  processOutput(p: ts.PropertyDeclaration): void {
    const initializer = p.initializer!;
    if (ts.isNewExpression(initializer)) {
      const name = p.name.getText();
      const type = initializer.typeArguments![0].getText();

      const outputProp = new pb.OutputProp();
      outputProp.setDocs(this.getJsDoc(p));
      outputProp.setName(name);
      outputProp.setEventName(this.formatEventName(name));
      // If the type is simple, then we compute based on the name
      // else, we use the type directly
      const simpleType = this.getSimpleType(type);
      const jsType = new pb.JsType();
      jsType.setIsPrimitive(!!simpleType);
      jsType.setTypeName(type);
      outputProp.setEventJsType(jsType);
      if (simpleType) {
        const eventProp = new pb.Prop();
        eventProp.setName(name.replace('Change', ''));
        const xType = new pb.XType();
        xType.setSimpleType(simpleType);
        eventProp.setType(xType);
        outputProp.addEventProps(eventProp);
      } else {
        // Need to import complex type.
        this.input.getNgModulesList()[0].addOtherSymbols(type);
        outputProp.setEventPropsList(this.getEventProps(type));
      }
      this.proto.addOutputProps(outputProp);
    }
  }

  getEventProps(type: string): pb.Prop[] {
    for (const statement of this.sourceFile.statements) {
      if (ts.isClassDeclaration(statement)) {
        const cls = statement;
        if (cls.name?.getText() === type) {
          const eventProps: pb.Prop[] = [];
          for (const member of cls.members) {
            if (ts.isPropertyDeclaration(member)) {
              const property = member;
              const simpleType = this.getSimpleType(property.type?.getText()!);
              if (simpleType) {
                const eventProp = new pb.Prop();
                eventProp.setName(property.name.getText());
                const typeProto = new pb.XType();
                typeProto.setSimpleType(simpleType);
                eventProp.setType(typeProto);
                eventProp.setDocs(this.getJsDoc(property));
                eventProps.push(eventProp);
              } else {
                // Deliberately ignore since we can't transmit something like an element
                // reference through our protocol.
              }
            }
          }

          return eventProps;
        }
      }
    }
    this.logIssue("Didn't get event props", {event: type});
    return [];
  }

  formatEventName(name: string): string {
    let str = capitalize(name) + 'Event';
    if (name !== capitalize(name)) {
      str = upperCamelCase(this.input.getName()) + str;
    }
    if (str.startsWith('Mat')) {
      str = str.slice(3);
    }
    return str;
  }

  formatPropName(name: string): string {
    return capitalize(name);
  }

  getType(type: ts.TypeNode, initializer?: ts.Expression): pb.XType {
    const text = type.getText();
    // e.g. badge's content property has a very open union type,
    // pick string since it's the most flexible. We don't support
    // complex union types in the XType proto (and we can always coerce)
    // a number to string if needed in py.
    if (text === 'string | number | undefined | null') {
      const typeProto = new pb.XType();
      typeProto.setSimpleType(pb.SimpleType.STRING);
      return typeProto;
    }
    const segments = text
      .split('|')
      .map((s) => s.trim())
      .filter((s) => ['null', 'undefined'].every((val) => val !== s));
    const simpleTypes = segments.map((s) => this.getSimpleType(s));
    if (simpleTypes.length === 1) {
      const typeProto = new pb.XType();
      if (simpleTypes[0]) {
        typeProto.setSimpleType(simpleTypes[0]);
      } else {
        // Maybe it's a type alias
        if (this.typeAliasMap.has(text)) {
          return this.typeAliasMap.get(text)!;
        } else {
          this.logIssue('Unhandled single type', {type: text});
        }
      }
      return typeProto;
    } else {
      // We assume these are string literals.
      const stringLiterals = segments
        // Filter out empty string due to a leading "|" for long union types.
        .filter((x) => x)
        .map(this.stripQuotes);
      const typeProto = new pb.XType();
      const sl = new pb.StringLiterals();
      sl.setStringLiteralList(stringLiterals);
      if (!initializer) {
        // Special case for FloatLabelType (from form-field); it's hard to infer, but the default is 'auto'
        // which breaks the convention.
        if (type.getText() === "'always' | 'auto'") {
          sl.setDefaultValue('auto');
        } else {
          // If there's no initializer, then we just pick the first value (somewhat arbitrary, but
          // Angular Material seemes to default to it).
          sl.setDefaultValue(stringLiterals[0]);
        }
      } else {
        sl.setDefaultValue(this.stripQuotes(initializer.getText()));
      }
      typeProto.setStringLiterals(sl);
      return typeProto;
    }
  }

  getSimpleType(type: string): pb.SimpleTypeMap[keyof pb.SimpleTypeMap] | null {
    switch (type) {
      case 'string':
        return pb.SimpleType.STRING;
      case 'boolean':
        return pb.SimpleType.BOOL;
      case 'number':
        return pb.SimpleType.NUMBER;
      default:
        return null;
    }
  }

  stripQuotes = (t: string): string => {
    // Strip off quotes (but sanity check first)
    if (t[0] !== "'" && t[t.length - 1] !== "'") {
      this.logIssue('Unexpected type', {string: t});
      return '<issue>';
    }
    return t.slice(1, -1);
  };

  getJsDoc(node: ts.Node): string {
    const jsDocs = ts.getJSDocCommentsAndTags(node);
    return jsDocs
      .map((d) => d.getText())
      .join(' ')
      .split('/**')
      .join('')
      .split('*/')
      .join('')
      .replace(/[\s]+\*/g, '')
      .trim();
  }
}

function main() {
  const args = parseArgs();
  const workspaceRoot = args['workspace_root'];
  if (!workspaceRoot) {
    throw new Error(
      'Must set --workspace_root (path to Bazel workspace directory)',
    );
  }
  if (args['dry_run']) {
    console.log('Running in dry mode.');
  }
  for (const specInput of SPEC_INPUTS) {
    let filename = `${kebabCase(specInput.getName())}.ts`;
    if (specInput.getTsFilename()) {
      filename = specInput.getTsFilename();
    }
    const inputFilePath = path.join(
      workspaceRoot,
      'third_party',
      'angular_components',
      'src',
      'material',
      kebabCase(specInput.getName()),
      filename,
    );

    const parser = new NgParser(specInput, inputFilePath);

    // console.log(JSON.stringify(parser.proto.toObject(), null, 2));

    if (parser.validate() && workspaceRoot) {
      const out_path = path.join(workspaceRoot, 'generator', 'output_data');
      fs.writeFileSync(
        path.join(out_path, `${parser.proto.getInput()!.getName()}.json`),
        JSON.stringify(parser.proto.toObject(), null, 2),
      );
      fs.writeFileSync(
        path.join(out_path, `${parser.proto.getInput()!.getName()}.binarypb`),
        parser.proto.serializeBinary(),
      );
    }
  }
}

main();
