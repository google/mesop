function resolveOptic(resolveDir, path) {
  const binIndex = resolveDir.indexOf('/bin/');
  if (binIndex === -1) {
    throw new Error('Expected to find /bin/ in ' + resolveDir);
  }

  // Extract the part of the string up to and including "/bin/"
  const upUntilBin = resolveDir.substring(0, binIndex + '/bin/'.length);

  const result =
    upUntilBin +
    // "optic/" is our workspace name (and not an actual file directory)
    // so we remove it as a prefix.
    path.substring('optic/'.length) +
    // Generated protos are ".js" files
    '.js';

  return result;
}

// Handles imports to generated proto files.
let opticProtoOnResolvePlugin = {
  name: 'optic-proto',
  setup(build) {
    build.onResolve({filter: /^optic\//}, (args) => {
      return {path: resolveOptic(args.resolveDir, args.path)};
    });
  },
};

export default {
  resolveExtensions: ['.js'],
  format: 'esm',
  plugins: [opticProtoOnResolvePlugin],
};
