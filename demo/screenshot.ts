import {test, expect} from '@playwright/test';

import * as fs from 'fs';
import * as path from 'path';

// Filter for Python files (.py extension)
const pythonDemoFiles = fs
  .readdirSync(__dirname)
  .filter((file) => path.extname(file) === '.py');

console.log(pythonDemoFiles);

// Remove the skip if you want to re-generate the screenshots.
test.skip('screenshot each demo', async ({page}) => {
  // This will take a while.
  test.setTimeout(0);

  await page.setViewportSize({width: 400, height: 300});

  for (const demoFile of pythonDemoFiles) {
    const demo = demoFile.slice(0, -3);
    await page.goto('/' + demo);
    await new Promise((resolve) => setTimeout(resolve, 3000));
    // Take a full-page screenshot
    await page.screenshot({
      path: `demo/screenshots/${demo}.png`,
      fullPage: true,
    });
  }
});
