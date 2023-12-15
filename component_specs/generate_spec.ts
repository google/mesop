import ts from 'typescript';
// @ts-ignore
import fs from 'fs';
import path from 'path';

import * as pb from './component_spec_jspb_proto_pb/component_specs/component_spec_pb';

/**
 * Event properties.
 *
 * Content. OK (manual)
 */

// TO DO: not hard code
const TARGET_CLASS_NAME = 'MatCheckbox';

const SPEC = new pb.ComponentSpecInput();
SPEC.setName('checkbox');
SPEC.setFilePath(
  '/Users/will/Documents/GitHub/mesop/component_specs/input_data/checkbox.ts',
);
SPEC.setTargetClass('MatCheckbox');
SPEC.setHasContent(true);

interface Issue {
  msg: string;
  context: any;
  node: any;
}

class NgParser {
  proto: pb.ComponentSpec;
  private issues: Issue[] = [];
  private currentNode!: ts.Node;
  sourceFile!: ts.SourceFile;
  constructor(private readonly input: pb.ComponentSpecInput) {
    this.proto = new pb.ComponentSpec();
    this.proto.setInput(input);
    this.parseTs(this.input.getFilePath());
  }

  parseTs(filePath: string) {
    // Read the TypeScript file
    const fileContents = fs.readFileSync(filePath, 'utf8');

    // Parse the file contents into a TypeScript AST
    this.sourceFile = ts.createSourceFile(
      filePath,
      fileContents,
      ts.ScriptTarget.Latest,
      true, // setParentNodes flag
    );

    this.sourceFile.statements.find((s) => {
      if (ts.isClassDeclaration(s)) {
        if (s.name?.escapedText === this.input.getTargetClass()) {
          this.processClass(s);
        }
      }
    });
  }

  logIssue(msg: string, context?: object | string) {
    this.issues.push({msg, context, node: this.currentNode?.getText()});
  }

  validate(): boolean {
    const FgRed = '\x1b[31m';
    const FgGreen = '\x1b[32m';
    const Reset = '\x1b[0m';

    if (this.issues.length) {
      console.error(FgRed, '========================');
      console.error(FgRed, this.issues.length + ' issues found', Reset);
      for (const issue of this.issues) {
        console.error(issue.msg, issue.context, issue.node);
      }
      return false;
    } else {
      console.log(FgGreen, 'Validation succeeded!');
      return true;
    }
  }

  processClass(cls: ts.ClassDeclaration) {
    for (const member of cls.members) {
      if (!ts.isPropertyDeclaration(member)) {
        continue;
      }
      const prop = member as ts.PropertyDeclaration;
      this.currentNode = prop;
      if (!prop.modifiers) {
        continue;
      }
      for (const modifier of prop.modifiers) {
        if (ts.isDecorator(modifier)) {
          const decorator = modifier as ts.Decorator;
          if (ts.isCallExpression(decorator.expression)) {
            const callExpression = decorator.expression;
            if (ts.isIdentifier(callExpression.expression)) {
              const identifier = callExpression.expression as ts.Identifier;
              if (identifier.escapedText === 'Input') {
                this.processInput(prop);
              } else if (identifier.escapedText === 'Output') {
                this.processOutput(prop);
              }
            }
          }
        }
      }
    }
  }

  processInput(m: ts.PropertyDeclaration): void {
    this.currentNode = m;
    // these are property claration which are input
    const prop = m as ts.PropertyDeclaration;
    const name = prop.name;
    if (ts.isIdentifier(name)) {
      const elName = name.escapedText.toString();
      const elProp = new pb.ElementProp();
      elProp.setKey(elName);
      const propBinding = new pb.PropertyBinding();
      propBinding.setName(elName);
      propBinding.setDebugType(prop.type!.getText());
      propBinding.setType(this.getType(assert(prop.type)));
      elProp.setPropertyBinding(propBinding);
      this.proto.addProps(elProp);
    } else {
      throw new Error('Expected identifier for prop' + prop);
    }
  }

  processOutput(p: ts.PropertyDeclaration): void {
    const initializer = p.initializer!;
    if (ts.isNewExpression(initializer)) {
      const name = p.name.getText();
      const type = initializer.typeArguments![0].getText();

      const elProp = new pb.ElementProp();
      elProp.setKey(name);
      const eventBinding = new pb.EventBinding();
      // If the type is simple, then we compute based on the name
      // else, we use the type directly
      const simpleType = this.getSimpleType(type);
      if (simpleType) {
        eventBinding.setEventName(this.formatEventName(name));
        const eventProp = new pb.EventProp();
        eventProp.setKey(name.replace('Change', ''));
        const type = new pb.JsType();
        type.setSimpleType(simpleType);
        eventProp.setType(type);
        eventBinding.addProps(eventProp);
      } else {
        eventBinding.setEventName(this.formatEventName(type));
        eventBinding.setPropsList(this.getEventProps(type));
      }
      elProp.setEventBinding(eventBinding);
      this.proto.addProps(elProp);
    }
  }
  getEventProps(type: string): pb.EventProp[] {
    for (const statement of this.sourceFile.statements) {
      if (ts.isClassDeclaration(statement)) {
        const cls = statement;
        if (cls.name?.getText() === type) {
          const eventProps: pb.EventProp[] = [];
          // This is the right one;
          for (const member of cls.members) {
            if (ts.isPropertyDeclaration(member)) {
              const property = member;
              const simpleType = this.getSimpleType(property.type?.getText()!);
              if (simpleType) {
                const eventProp = new pb.EventProp();
                eventProp.setKey(property.name.getText());
                const typeProto = new pb.JsType();
                typeProto.setSimpleType(simpleType);
                eventProp.setType(typeProto);
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

  getType(type: ts.TypeNode): pb.JsType {
    const text = type.getText();
    const segments = text
      .split('|')
      .map((s) => s.trim())
      .filter((s) => ['null', 'undefined'].every((val) => val !== s));
    const simpleTypes = segments.map((s) => this.getSimpleType(s));
    if (simpleTypes.length === 1) {
      const typeProto = new pb.JsType();
      if (simpleTypes[0]) {
        typeProto.setSimpleType(simpleTypes[0]);
      } else {
        this.logIssue('Unhandled simple type', {type: simpleTypes[0]});
      }
      return typeProto;
    } else {
      // We asumme these are string literals.
      const stringLiterals = segments.map((t) => {
        // Strip of quotes (but sanity check first)
        if (t[0] !== "'" && t[t.length - 1] !== "'") {
          this.logIssue('Unexpected type', {type: text});
          return '<issue>';
        }
        return t.slice(1, -1);
      });
      const typeProto = new pb.JsType();
      const sl = new pb.StringLiterals();
      sl.setStringLiteralList(stringLiterals);
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
}

function assert<T>(value: T | null | undefined): T {
  if (value === null || value === undefined) {
    throw new Error('Asserted value is null or undefined');
  }
  return value;
}

function main() {
  const parser = new NgParser(SPEC);
  console.log(JSON.stringify(parser.proto.toObject(), null, 2));
  if (parser.validate()) {
    // Write parser proto to file "output_data/${proto.name}"
    fs.writeFileSync(
      path.join(
        parser.proto.getInput()?.getFilePath()!,
        '..',
        '..',
        'output_data',
        `${parser.proto.getInput()!.getName()}.json`,
      ),
      JSON.stringify(parser.proto.toObject(), null, 2),
    );
  }
}

function capitalize(string: string): string {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function upperCamelCase(string: string): string {
  return string
    .split('_')
    .map((s) => capitalize(s))
    .join('');
}

main();
