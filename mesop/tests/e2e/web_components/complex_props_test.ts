import {test, expect} from '@playwright/test';

test('web components - complex properties (array and object)', async ({
  page,
}) => {
  await page.goto('/web_component/complex_props/complex_props_app');
  // Make sure page is loaded.
  await expect(page.getByText('Loaded')).toBeVisible();

  // Make sure values from array is displayed:
  await expect(page.getByText('element1')).toBeVisible();
  // Make sure values from object is displayed:
  await expect(page.getByText('key1: value1')).toBeVisible();
});
