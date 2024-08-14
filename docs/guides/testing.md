# Testing

This guide covers the recommended approach for testing Mesop applications using Playwright, a popular browser automation and testing framework.

However, you can use any other testing framework and there's no official testing framework for Mesop.

## Testing Philosophy

Because Mesop is a full-stack UI framework we recommend doing integration tests to cover critical app functionality. We also recommend separating core business logic into separate Python modules, which do not depend on Mesop. This way you can easily unit test your business logic as well as reuse the business logic as part of scripts or other binaries besides Mesop.

## Playwright Example

We will walk through [mesop-playwright-testing repo](https://github.com/wwwillchen/mesop-playwright-testing) which contains a simple Mesop counter app and a Playwright test written in TypeScript (node.js). Although [Playwright has a Python flavor](https://playwright.dev/python/), we recommend using the Playwright node.js flavor because it has better testing support. Even if you're not familiar with JavaScript or TypeScript, it's extremely easy to write Playwright tests because you can [generate your tests](https://playwright.dev/docs/codegen-intro) by clicking through the UI.

The testing example repo's [README.md](https://github.com/wwwillchen/mesop-playwright-testing?tab=readme-ov-file#mesop-playwright-testing-example) contains instructions for setting up your environment and running the tests.

### Playwright config

The playwright configuration used is similar to the [default one](https://playwright.dev/docs/intro#installing-playwright), however we change a few configurations specific for Mesop.

For example, in [`playwright.config.ts`](https://github.com/wwwillchen/mesop-playwright-testing/blob/main/playwright.config.ts), we configure Mesop as the local dev server:

```ts
  webServer: {
    command: "mesop app.py",
    url: "http://127.0.0.1:32123",
    reuseExistingServer: !process.env.CI,
  },
```

This will launch the Mesop app server at the start of the tests.

We also added the following configurations to make writing and debugging tests easier:

```ts
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: "http://127.0.0.1:32123",

    /* See https://playwright.dev/docs/trace-viewer */
    trace: "retain-on-failure",

    // Capture screenshot after each test failure.
    screenshot: "on",

    // Retain video on test failure.
    video: "retain-on-failure",
  },
```

### Running and debugging a test

Try changing the test so that it fails. For example, in [`app.spec.ts`](https://github.com/wwwillchen/mesop-playwright-testing/blob/main/tests/app.spec.ts) change `"Count=1"` to `"Count=2"` and then run the tests: `npx playwright test`.

The test will fail (as expected) and a new browser page should be opened with the test failure information. You can click on the failing test and view the screenshot, video and trace. This is very helpful in figuring out why a test failed.

### Writing a test

As mentioned above, it's very easy to write Playwright tests because you can [generate your tests](https://playwright.dev/docs/codegen-intro) by clicking through the UI. Even if you're not familiar with JavaScript/TypeScript, you will be able to generate most of the test code by clicking through the UI and copying the generated test code.

???+ tip "Use the [Playwright VS Code extension](https://playwright.dev/docs/getting-started-vscode)"

    You can use the Playwright VS Code extension to directly generate test code in your file. You can also run and debug tests from VS Code as well.

## Learn more

We recommend reading [Playwright's docs](https://playwright.dev) which are easy to follow and contain much more information on writing browser tests.

You can also look at Mesop's [own tests](https://github.com/google/mesop/tree/main/mesop/tests/e2e) written with Playwright.
