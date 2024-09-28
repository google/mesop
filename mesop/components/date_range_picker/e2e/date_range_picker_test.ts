import {test, expect} from '@playwright/test';

test('start date input', async ({page}) => {
  await page.goto('/components/date_range_picker/e2e/date_range_picker_app');

  // Enter valid start date
  const startDateInput = page.locator('//input[@placeholder="9/1/2024"]');
  await startDateInput.click();
  await startDateInput.fill('9/10/2024');
  await page.getByText('Start date: ').click();
  await expect(page.getByText('Start date: 2024-09-10')).toBeVisible();

  // Enter invalid start date
  await startDateInput.click();
  await startDateInput.fill('13/10/2024');
  await page.getByText('Start date: 2024-09-10').click();
  await expect(page.getByText('Start date: 2024-09-10')).toBeVisible();
});

test('end date input', async ({page}) => {
  await page.goto('/components/date_range_picker/e2e/date_range_picker_app');

  // Enter valid end date
  const endDateInput = page.locator('//input[@placeholder="10/1/2024"]');
  await endDateInput.click();
  await endDateInput.fill('12/10/2024');
  await page.getByText('End date: ').click();
  await expect(page.getByText('End date: 2024-12-10')).toBeVisible();

  // Enter invalid end date
  await endDateInput.click();
  await endDateInput.fill('13/10/2024');
  await page.getByText('End date: 2024-12-10').click();
  await expect(page.getByText('End date: 2024-12-10')).toBeVisible();
});

test('date range picker', async ({page}) => {
  await page.goto('/components/date_range_picker/e2e/date_range_picker_app');

  await page.locator('//button').click();
  await page.locator('//button/span[text()=" 15 "]').click();

  // Unchanged until end date is selected.
  await expect(page.getByText('Start date: 2024-10-01')).toBeVisible();
  await expect(page.getByText('End date: 2024-11-01')).toBeVisible();

  await page.locator('//button/span[text()=" 28 "]').click();

  // Updated after end date selected.
  await expect(page.getByText('Start date: 2024-10-15')).toBeVisible();
  await expect(page.getByText('End date: 2024-10-28')).toBeVisible();
});
