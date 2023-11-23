import { defineConfig, devices } from "@playwright/test";

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  timeout: 5000,
  testDir: ".",
  testMatch: "e2e/*_test.ts",
  testIgnore: "scripts/**",
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  retries: 2,
  /* Force non-parallelism due to flakiness. */
  workers: 1,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: "html",
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: "http://127.0.0.1:8080/",

    /* See https://playwright.dev/docs/trace-viewer */
    trace: "retain-on-failure",

    // Capture screenshot after each test failure.
    screenshot: "on",

    video: "retain-on-failure",
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  /* Run your local dev server before starting the tests */
  webServer: {
    command: "bazel run //optic/cli -- --path=optic/testing/index.py --ci",
    url: "http://127.0.0.1:8080/",
    reuseExistingServer: !process.env.CI,
  },
});
