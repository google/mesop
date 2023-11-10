# Development

## Build

We use [Bazel](https://bazel.build/) as our build system.

## Python

### Run dev-server

```
$ ibazel run //optic:cli -- --path="optic/examples/simple.py"
```

### Third-party packages (PIP)

If you update `//optic/requirements.txt`, run:

```
$ bazel run //optic:pip_requirements.update
```

### Run tests

```
bazel run //tests/...:all
```

### venv / VS Code

To support IDE type-checking (Pylance) in VS Code, we use Aspect's [rules_py](https://docs.aspect.build/rulesets/aspect_rules_py/) which generates a venv target.

```
$ bazel run //optic:dev_server.venv
```

Then, you can activate the venv:

```
$ source .dev_server.venv/bin/activate
```

You will need to setup a symlink to have Python IDE support for protos:

```
$ ./setup_proto_symlink.sh
```

Check that you're using venv's python:

```
$ which python
```

Copy the python interpreter path and paste it into VS Code.

Finally, install third-party dependencies.

```
$ pip install -r optic/requirements_lock.txt
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