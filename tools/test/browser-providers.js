// Forked from: https://github.com/angular/components/blob/8ac3ca11add4ae194b2b79169559fb3dbad7e161/test/browser-providers.js

/*
 * Browser Configuration for the different jobs in the legacy Karma tests.
 *
 *   - `browserstack`: Launches the browser within BrowserStack
 *   - `saucelabs`: Launches the browser within Saucelabs
 */
const browserConfig = {
  'iOS15': {unitTest: {target: 'saucelabs'}},
  'Safari15': {unitTest: {target: 'browserstack'}},
};

/** Exports all available custom Karma browsers. */
exports.customLaunchers = require('./karma-browsers.json');

/** Exports a map of configured browsers, which should run in the given platform. */
exports.platformMap = {
  'saucelabs': buildConfiguration('unitTest', 'saucelabs'),
  'browserstack': buildConfiguration('unitTest', 'browserstack'),
};

/** Build a list of configuration (custom launcher names). */
function buildConfiguration(type, target) {
  const targetBrowsers = Object.keys(browserConfig)
    .map((browserName) => [browserName, browserConfig[browserName][type]])
    .filter(([, config]) => config.target === target)
    .map(([browserName]) => browserName);

  return targetBrowsers.map(
    (browserName) => `${target.toUpperCase()}_${browserName.toUpperCase()}`,
  );
}
