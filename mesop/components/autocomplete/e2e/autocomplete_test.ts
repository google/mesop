import {test, expect} from '@playwright/test';

test('Autocomplete Alaska', async ({page}) => {
  await page.goto('/components/autocomplete/e2e/autocomplete_app');
  await page.locator('//input').fill('A');
  await expect(page.getByRole('option', {name: 'Arizona'})).toBeAttached();
  await expect(page.getByRole('option', {name: 'Alaska'})).toBeAttached();
  await page.locator('//input').fill('Al');
  await expect(page.getByRole('option', {name: 'Arizona'})).not.toBeAttached();
  await page.getByRole('option', {name: 'Alaska'}).click();
  await expect(page.getByText('Selected: Alaska')).toBeAttached();
  await page.locator('//input').fill('CALI');
  await page.getByRole('option', {name: 'California'}).click();
  await expect(page.getByText('Selected: California')).toBeAttached();
});
