# Modes

There are two modes that you can run Mesop in.

## Development mode (aka debug mode or editor mode)

Recommended for developers using Mesop when they are developing the apps locally. This provides good error messages and hot reloading.

- **How to run:** `ibazel run //mesop/cli -- --path=mesop/mesop/example_index.py`
- Angular should run in dev mode.
- Developer Tools and Visual Editor are available.

## Prod mode

Recommended when developers deploy applications built with Mesop for public serving. This is optimized for performance and provides less-detailed error messages.

- Developer tools aren't available.
- Angular doesn't run in dev mode.
- **How to run:** `bazel run //mesop/cli -- --path=mesop/mesop/example_index.py --prod`
