import ts from 'typescript';
import fs from 'fs';

import {ComponentSpec} from './component_spec_jspb_proto_pb/component_specs/component_spec_pb';

// TO DO: not hard code
const TARGET_CLASS_NAME = 'MatCheckbox';

class NgParser {
  proto: ComponentSpec;

  constructor(
    private readonly filePath: string,
    private readonly targetClassName: string,
  ) {
    this.proto = new ComponentSpec();
  }

  parseTs(filePath: string) {
    // Read the TypeScript file
    const fileContents = fs.readFileSync(filePath, 'utf8');

    // Parse the file contents into a TypeScript AST
    const sourceFile = ts.createSourceFile(
      filePath,
      fileContents,
      ts.ScriptTarget.Latest,
      true, // setParentNodes flag
    );

    sourceFile.statements.find((s) => {
      if (ts.isClassDeclaration(s)) {
        if (s.name?.escapedText === this.targetClassName) {
          this.processClass(s);
        }
      }
    });
  }

  processClass(cls: ts.ClassDeclaration) {
    console.log(
      cls.members
        .filter((m) => {
          return ts.isPropertyDeclaration(m);
        })
        .filter((m) => {
          const prop = m as ts.PropertyDeclaration;
          const inputMod = prop.modifiers?.find((mod) => {
            if (ts.isDecorator(mod)) {
              const decorator = mod as ts.Decorator;
              if (ts.isCallExpression(decorator.expression)) {
                const callExpression = decorator.expression;
                if (ts.isIdentifier(callExpression.expression)) {
                  const identifier = callExpression.expression as ts.Identifier;
                  return identifier.escapedText === 'Input';
                }
              }
            }
            return;
          });
          return inputMod;
        })
        .map((m) => {
          // these are property claration which are input
          const prop = m as ts.PropertyDeclaration;
          const name = prop.name;
          if (ts.isIdentifier(name)) {
            return {name: name.escapedText, type: getType(assert(prop.type))};
          } else {
            throw new Error('Expected identifier for prop' + prop);
          }
        }),
    );
  }
}

function getType(type: ts.TypeNode) {
  return type.getText();
}

function parseCommandLineArguments(): {[flag: string]: string} {
  const args = process.argv.slice(2); // Remove the first two default entries
  const argsMap: {[flag: string]: string} = {};
  args.forEach((val, index) => {
    if (val.startsWith('--')) {
      const segments = val.split('=');
      argsMap[segments[0].slice('--'.length)] = segments[1];
    }
  });
  return argsMap;
}

function assert<T>(value: T | null | undefined): T {
  if (value === null || value === undefined) {
    throw new Error('Asserted value is null or undefined');
  }
  return value;
}

function main() {
  const argsMap = parseCommandLineArguments();
  const filePath = argsMap['path'];

  if (!filePath) {
    console.error('Please provide a file path using the --path flag');
    process.exit(1);
  }
  const parser = new NgParser(filePath, TARGET_CLASS_NAME);
  console.log('OUT:', parser.proto);
}

main();
