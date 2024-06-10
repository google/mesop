import {defineConfig, devices} from '@playwright/test';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

// We need to run all tests with component tree diffs enabled and disabled.
// We use this flag to toggle between the two modes.
const enableComponentTreeDiffs = process.env.ENABLE_COMPONENT_TREE_DIFFS
  ? '--enable_component_tree_diffs'
  : '--noenable_component_tree_diffs';

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  timeout: process.env.CI ? 20000 : 10000, // Budget more time for CI since tests run slower there.
  testDir: '.',
  // Use a custom snapshot path template because Playwright's default
  // is platform-specific which isn't necessary for Mesop e2e tests
  // which should be platform agnostic (we don't do screenshots; only textual diffs).
  snapshotPathTemplate:
    '{testDir}/{testFileDir}/snapshots/{testFileName}_{arg}{ext}',

  testMatch: ['e2e/*_test.ts', 'demo/screenshot.ts'],
  testIgnore: 'scripts/**',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://127.0.0.1:32123/',

    /* See https://playwright.dev/docs/trace-viewer */
    trace: 'retain-on-failure',

    // Capture screenshot after each test failure.
    screenshot: 'on',

    video: 'retain-on-failure',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: {...devices['Desktop Chrome']},
    },
  ],

  /* Run your local server before starting the tests */
  webServer: {
    command: `bazel run //mesop/cli -- --path=mesop/mesop/example_index.py --prod ${enableComponentTreeDiffs}`,
    url: 'http://127.0.0.1:32123/',
    reuseExistingServer: !process.env.CI,
  },
});
