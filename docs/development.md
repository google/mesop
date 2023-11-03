# Development

## Build

We use [Bazel](https://bazel.build/) as our build system.

## Python

### Third-party packages (PIP)

If you update `//optic/requirements.txt`, run:

```
$ bazel run //optic:pip_requirements.update
```

### Run tests

```
bazel run //tests/...:all
```

## Commit hooks

We use [pre-commit](https://pre-commit.com/) to automatically format, lint code before committing.

*Setup:*

1. [Install pre-commit](https://pre-commit.com/#installation).
1. Setup git hook: ```pre-commit install```

## Web (Angular)

### Run local dev server

```
ibazel run //web/src/app:devserver
```

> NOTE: this will automatically reload the browser when an edit is made.