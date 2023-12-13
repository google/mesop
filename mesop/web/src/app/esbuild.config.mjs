function resolveMesop(resolveDir, path) {
  const binIndex = resolveDir.indexOf('/bin/');
  if (binIndex === -1) {
    throw new Error('Expected to find /bin/ in ' + resolveDir);
  }

  // Extract the part of the string up to and including "/bin/"
  const upUntilBin = resolveDir.substring(0, binIndex + '/bin/'.length);

  const result =
    upUntilBin +
    // "mesop/" is our workspace name (and not an actual file directory)
    // so we remove it as a prefix.
    path.substring('mesop/'.length) +
    // Generated protos are ".js" files
    '.js';

  return result;
}

// Handles imports to generated proto files.
let mesopProtoOnResolvePlugin = {
  name: 'mesop-proto',
  setup(build) {
    build.onResolve({filter: /^mesop\//}, (args) => {
      return {path: resolveMesop(args.resolveDir, args.path)};
    });
  },
};

export default {
  resolveExtensions: ['.js'],
  format: 'esm',
  plugins: [mesopProtoOnResolvePlugin],
};
