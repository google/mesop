# Testing

## Unit tests

You can run our unit tests using Bazel.

### Run tests

```sh
bazel test //mesop/...
```

## E2E tests

We use [Playwright](https://playwright.dev/) as our e2e test framework. Unlike most of the stack, this isn't Bazel-ified although we'd like to eventually do this.

### Run tests

```shell
yarn playwright test
```

### Debug tests

```shell
yarn playwright test --debug
```
