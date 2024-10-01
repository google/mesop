import {test, expect} from '@playwright/test';

test('date picker', async ({page}) => {
  await page.goto('/components/datepicker/e2e/datepicker_app');

  // Enter valid date
  await page.locator('//input').click();
  await page.locator('//input').fill('9/10/2024');
  await page.getByText('Selected date: ').click();
  await expect(page.getByText('Selected date: 2024-09-10')).toBeVisible();

  // Pick date from calendar
  await page.getByLabel('Open calendar').click();
  await page.locator('//button/span[text()=" 15 "]').click();
  await expect(page.getByText('Selected date: 2024-09-15')).toBeVisible();

  // Enter invalid date
  await page.locator('//input').click();
  await page.locator('//input').fill('13/10/2024');
  await page.getByText('Selected date: 2024-09-15').click();
  await expect(page.getByText('Selected date: 2024-09-15')).toBeVisible();
});
