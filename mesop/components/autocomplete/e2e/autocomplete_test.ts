import {test, expect} from '@playwright/test';

test('Autocomplete Alaska', async ({page}) => {
  await page.goto('/components/autocomplete/e2e/autocomplete_app');
  await expect(await page.locator('//input').inputValue()).toEqual(
    'California',
  );

  // Filter to A
  await page.locator('//input').fill('A');
  await expect(page.getByRole('option', {name: 'Arizona'})).toBeAttached();
  await expect(page.getByRole('option', {name: 'Alaska'})).toBeAttached();

  // Filter Al
  await page.locator('//input').fill('Al');
  await expect(page.getByRole('option', {name: 'Arizona'})).not.toBeAttached();
  await page.getByRole('option', {name: 'Alaska'}).click();
  await expect(page.getByText('Selected: Alaska')).toBeAttached();

  // Filter uppercase works
  await page.locator('//input').fill('CALI');
  await page.getByRole('option', {name: 'California'}).click();
  await expect(page.getByText('Selected: California')).toBeAttached();

  // Enter works for selection
  await page.locator('//input').fill('Penn');
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Enter');
  await expect(await page.getByText('Selected: Pennsylvania')).toBeAttached();

  // Enter works for populating free text
  await page.locator('//input').fill('Test');
  await page.keyboard.press('Enter');
  await expect(await page.getByText('Selected: Test')).toBeAttached();
});
