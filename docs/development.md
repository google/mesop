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
