export function capitalize(string: string): string {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function upperCamelCase(string: string): string {
  return string
    .split('_')
    .map((s) => capitalize(s))
    .join('');
}

export function kebabCase(str: string): string {
  return str.split('_').join('-');
}

export function assert<T>(value: T | null | undefined): T {
  if (value === null || value === undefined) {
    throw new Error('Asserted value is null or undefined');
  }
  return value;
}

/** Parser function for '--arg=value' format */
export const parseArgs = (): {[key: string]: string | undefined} => {
  // @ts-ignore
  const args: string[] = process.argv.slice(2);
  const parsedArgs: {[key: string]: string | undefined} = {};

  args.forEach((arg) => {
    // Split each argument into key and value
    const [key, value] = arg.split('=');

    // Remove the leading '--' from the key and add to the object
    if (key.startsWith('--')) {
      parsedArgs[key.slice('--'.length)] = value;
    }
  });

  return parsedArgs;
};
