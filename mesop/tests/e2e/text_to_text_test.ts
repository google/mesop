import {test, expect} from '@playwright/test';

test('text to text', async ({page}) => {
  await page.goto('/testing/text_to_text');
  const inputLocator = page.locator('#mat-input-0');
  await inputLocator.click();
  await inputLocator.fill('fly');
  // Need to wait for the input state to be saved before clicking.
  await page.waitForTimeout(2000);
  await page.getByRole('button', {name: 'Generate'}).click();
  await expect(page.getByText('Echo: fly')).toBeVisible();

  await inputLocator.click();
  await inputLocator.fill('abc');
  // Need to wait for the input state to be saved before clicking.
  await page.waitForTimeout(2000);
  await page.getByRole('button', {name: 'Generate'}).click();
  await expect(page.getByText('Echo: abc')).toBeVisible();
});
