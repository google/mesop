import {test, expect} from '@playwright/test';

test('is_target', async ({page}) => {
  await page.goto('/testing/click_is_target');
  await expect(page.getByText('Box clicked: False')).toBeVisible();
  await expect(page.getByText('Button clicked: False')).toBeVisible();

  await page.getByRole('button', {name: 'Click'}).click();
  await expect(page.getByText('Box clicked: False')).toBeVisible();
  await expect(page.getByText('Button clicked: True')).toBeVisible();

  (
    await page.locator(
      '//component-renderer[contains(@style, "background: red")]',
    )
  ).click();
  await expect(page.getByText('Box clicked: True')).toBeVisible();
  await expect(page.getByText('Button clicked: True')).toBeVisible();
});
