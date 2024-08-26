# Development

I recommend following (or at least reading) all the steps in this doc if you plan on actively developing Mesop.

## Setup

### Bazel/ibazel

We use [Bazel](https://bazel.build/) as our build system. Use [bazelisk](https://github.com/bazelbuild/bazelisk) which ensures the right version of Bazel is used for this project.

If [ibazel](https://github.com/bazelbuild/bazel-watcher) breaks, but bazel works, try following [these steps](https://github.com/bazelbuild/bazel-watcher/issues/588#issuecomment-1421939371)

> TIP: If your build mysteriously fails due to an npm-related error, try running `bazel clean --expunge && rm -rf node_modules`. Bazel and Yarn have a cache bug when upgrading npm modules.

### uv

We use [uv](https://github.com/astral-sh/uv). Follow the instructions [here](https://docs.astral.sh/uv/#getting-started) to install uv.

### Commit hooks

1. Install [pre-commit](https://pre-commit.com/#installation)
1. Install pre-commit hooks for this repo: `pre-commit install`

## Run local development

We recommend using this for most Mesop framework development.

```sh
./scripts/cli.sh
```

> NOTE: this automatically serves the angular app.

## Python

### Third-party packages (PIP)

If you update `//build_defs/requirements.txt`, run:

```sh
bazel run //build_defs:pip_requirements.update
```

### venv

To support IDE type-checking (Pylance) in VS Code, we use Aspect's [rules_py](https://docs.aspect.build/rulesets/aspect_rules_py/) which generates a venv target.

```sh
bazel run //mesop/cli:cli.venv
```

Then, you can activate the venv:

```sh
source .cli.venv/bin/activate
```

You will need to setup a symlink to have Python IDE support for protos:

```sh
./scripts/setup_proto_py_modules.sh
```

Check that you're using venv's python:

```sh
which python
```

Copy the python interpreter path and paste it into VS Code.

Finally, install third-party dependencies.

```sh
pip install -r build_defs/requirements_lock.txt
```

> NOTE: You may need to run the command with `sudo` if you get a permission denied error, particularly with "\_distutils_hack".

## Commit hooks

We use [pre-commit](https://pre-commit.com/) to automatically format, lint code before committing.

_Setup:_

1. [Install pre-commit](https://pre-commit.com/#installation).
1. Setup git hook: `pre-commit install`

## Docs

We use [Mkdocs Material](https://squidfunk.github.io/mkdocs-material/) to generate our docs site.

1. [Activate venv](#venv)
1. `mkdocs serve`
