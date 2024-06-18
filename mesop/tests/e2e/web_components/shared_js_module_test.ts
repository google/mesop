import {test, expect} from '@playwright/test';

test('web components - shared JS module', async ({page}) => {
  await page.goto('/web_component/shared_js_module/shared_js_module_app');
  expect(page.getByText('Loaded')).toBeVisible();
  expect(
    page.getByText('value from shared module: shared_module.js'),
  ).toBeVisible();
});
