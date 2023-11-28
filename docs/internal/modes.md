# Modes

There are several modes that you can run Optic in.

## Uncompiled mode

Only used for developing the Optic framework itself. Developers _using_ Optic shouldn't need to use this mode or be concerned about it.

- **How to run:** `$ scripts/run_py_dev.sh` and `$ scripts/run_web_dev.sh`
- Provides fast compile times, but requires two concurrent Bazel commands.
- Angular is run in dev mode.

## Debug mode

Recommended for developers using Optic when they are developing the apps locally. This provides good error messages and, in the future, will provide hot reloading.

- **How to run:** `$ bazel run //optic/cli -- --path=optic/testing/index.py --ci`
- Angular should run in dev mode.
- Developer Tools are available.

## Prod mode

Recommended when developers deploy applications built with Optic for public serving. This is optimized for performance and provides fairly opaque error messages.

- Developer tools aren't available.
- Angular doesn't run in dev mode.

<!-- TODO: Figure out what modes to run for `optic_binary` -->
