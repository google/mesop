import {test, expect} from '@playwright/test';

test('date picker', async ({page}) => {
  await page.goto('/components/datepicker/e2e/datepicker_app');
  // await page.locator('//input').nth(0).click();
  await page.locator('//input').nth(0).fill('9/10/2024');
  await page.locator('//input').nth(1).click();
  await expect(page.getByText('Selected date: 2024-09-10')).toBeVisible();
});
