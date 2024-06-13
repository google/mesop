import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/html/e2e/html_app');
  // checking if we can found any element with the text BOKEH_E2E_FIGURE
  expect(await page.textContent()).toContain('BOKEH_E2E_FIGURE');
});
