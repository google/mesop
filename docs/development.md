# Development

## Setup

### Bazel/ibazel

We use [Bazel](https://bazel.build/) as our build system. Use [bazelisk](https://github.com/bazelbuild/bazelisk) which ensures the right version of Bazel is used for this project.

If [ibazel](https://github.com/bazelbuild/bazel-watcher) breaks, but bazel works, try following [these steps](https://github.com/bazelbuild/bazel-watcher/issues/588#issuecomment-1421939371)

### Commit hooks

1. Install [pre-commit](https://pre-commit.com/#installation)
1. Install pre-commit hooks for this repo: `pre-commit install`

## Local Development

We recommend having two terminal tabs open because you will be running two processes for: 1. web and 2. python.

### Web Dev-server

```sh
$ ./scripts/run_web_dev.sh
```

> NOTE: this will automatically reload the browser when an edit is made.

### Python Server

```sh
$ ./scripts/run_py_dev.sh
```

> NOTE: if you do not include `--dev`, then it will default to prod mode.

## Prod mode

To run it in prod mode (which can be done locally or in an actual production environment), run the following:

```sh
$ bazel run //optic/cli -- --path="optic/examples/simple.py"
```

> NOTE: this automatically serves the angular app.

## Python

### Third-party packages (PIP)

If you update `//optic/requirements.txt`, run:

```sh
$ bazel run //optic:pip_requirements.update
```

### Run tests

```sh
bazel run //tests/...:all
```

### venv

To support IDE type-checking (Pylance) in VS Code, we use Aspect's [rules_py](https://docs.aspect.build/rulesets/aspect_rules_py/) which generates a venv target.

```sh
$ bazel run //optic/server:dev_server.venv
```

Then, you can activate the venv:

```sh
$ source .dev_server.venv/bin/activate
```

You will need to setup a symlink to have Python IDE support for protos:

```sh
$ ./setup_proto_symlink.sh
```

Check that you're using venv's python:

```sh
$ which python
```

Copy the python interpreter path and paste it into VS Code.

Finally, install third-party dependencies.

```sh
$ pip install -r optic/requirements_lock.txt
```

> NOTE: You may need to run the command with `sudo` if you get a permission denied error, particularly with "\_distutils_hack".

### Type-checking (pyright)

We use [pyright](https://github.com/microsoft/pyright) for type-checking our Python code because it has excellent IDE support (particularly for VS Code).

To run type-checking, please follow the above steps to setup the venv and activate it in your shell session.

**Pre-requisite:**

- You will need to run `$ setup_proto_py_modules.sh`.

**Command:**

```sh
$ pyright
```

## Commit hooks

We use [pre-commit](https://pre-commit.com/) to automatically format, lint code before committing.

_Setup:_

1. [Install pre-commit](https://pre-commit.com/#installation).
1. Setup git hook: `pre-commit install`

## Web (Angular)

<TODO>

## Docs

We use [Mkdocs Material](https://squidfunk.github.io/mkdocs-material/) to generate our docs site.

1. [Activate venv](#venv)
1. `mkdocs serve`
