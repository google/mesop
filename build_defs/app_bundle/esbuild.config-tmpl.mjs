/**
 * @license
 * Copyright Google LLC
 *
 * Use of this source code is governed by an MIT-style license that can be
 * found in the LICENSE file at https://angular.io/license
 *
 * Forked from: https://github.com/angular/dev-infra/blob/f82e2c46f5285375dd1944f29beae19849492f9a/bazel/app-bundling/esbuild.config-tmpl.mjs#L4
 */

import {createEsbuildAngularOptimizePlugin} from '@angular/build-tooling/shared-scripts/angular-optimization/esbuild-plugin.mjs';
import {GLOBAL_DEFS_FOR_TERSER_WITH_AOT} from '@angular/compiler-cli/private/tooling';
import * as path from 'path';

///////////////////////////////////
// Mesop-specific configurations
///////////////////////////////////
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

///////////////////////////////////
// End of Mesop-specific configurations
///////////////////////////////////

/** Root path pointing to the app bundle source entry-point file. */
const entryPointSourceRootPath = path.normalize(`TMPL_ENTRY_POINT_ROOTPATH`);

/**
 * Root path to the bundle entry-point without extension.
 *
 * The extension of the bundle entry-point file is not known because the ESBuild
 * rule strips the source extension (like `.ts`) and resolves the file based on
 * the resolved inputs.
 */
const entryPointBasepath = entryPointSourceRootPath.replace(/\.[^.]+$/, '');

/** Whether the given file is considered side-effect free. */
function isFileSideEffectFree(filePath) {
  // This returns false because proto-generated JS files which uses
  // the legacy closure module system get incorrectly optimized.
  return false;
}

export default {
  // Note: We prefer `.mjs` here as this is the extension used by Angular APF
  // packages.
  resolveExtensions: ['.mjs', '.js'],
  // Based on the CLI configuration:
  // https://github.com/angular/angular-cli/blame/8089c9388056b3caaf56f981848aca94f022da73/packages/angular_devkit/build_angular/src/tools/esbuild/application-code-bundle.ts#L51.
  conditions: ['es2022', 'es2020', 'es2015', 'module'],
  // Note: ES2015 main condition is needed for `rxjs@v6`.
  mainFields: ['fesm2022', 'es2022', 'es2020', 'es2015', 'module', 'main'],
  // The majority of these options match with the ones the CLI sets:
  // https://github.com/angular/angular-cli/blob/0d76bf04bca6e083865972b5398a32bbe9396e14/packages/angular_devkit/build_angular/src/webpack/plugins/javascript-optimizer-worker.ts#L133.
  treeShaking: true,
  pure: ['forwardRef'],
  legalComments: 'none',
  supported: {
    // We always downlevel `async/await` when bundling apps. The Angular CLI does the
    // same with its ESBuild experimental builder, and with the non-esbuild pipeline
    // Babel is used to downlevel async/await. See:
    // https://github.com/angular/angular-cli/blob/afe9feaa45913cbebe7f22c678d693d96f38584a/packages/angular_devkit/build_angular/src/babel/webpack-loader.ts#L111
    // https://github.com/angular/angular-cli/blob/afe9feaa45913/packages/angular_devkit/build_angular/src/builders/browser-esbuild/index.ts#L313-L318.
    'async-await': false,
  },
  // ESBuild requires the `define` option to take a string-based dictionary.
  define: convertObjectToStringDictionary(GLOBAL_DEFS_FOR_TERSER_WITH_AOT),
  plugins: [
    mesopProtoOnResolvePlugin,
    await createEsbuildAngularOptimizePlugin({
      optimize: {
        isSideEffectFree: isFileSideEffectFree,
      },
      downlevelAsyncGeneratorsIfPresent: true,
      enableLinker: {
        ensureNoPartialDeclaration: false,
        linkerOptions: {
          linkerJitMode: false,
        },
      },
    }),
  ],
};

/** Converts an object to a string dictionary. */
function convertObjectToStringDictionary(value) {
  return Object.entries(value).reduce((result, [propName, value]) => {
    result[propName] = String(value);
    return result;
  }, {});
}
