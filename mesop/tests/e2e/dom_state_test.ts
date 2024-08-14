import {test, expect} from '@playwright/test';

// Prevent regressions to:
// https://github.com/google/mesop/issues/371
test('navigation - resets DOM component state', async ({page}) => {
  await page.goto('/navigate_advanced/page1');
  await page.getByRole('checkbox').check();

  // Trigger a navigation.
  await page.getByRole('button', {name: 'navigate', exact: true}).click();

  // Make sure the navigation has finished
  await expect(page).toHaveURL('/navigate_advanced/page2');
  // The checkbox should be unchecked
  await expect(page.getByRole('checkbox')).not.toBeChecked();
});
