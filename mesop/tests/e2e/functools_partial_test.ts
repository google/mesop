import {test, expect} from '@playwright/test';

test('functools partial', async ({page}) => {
  await page.goto('/functools_partial');

  await page.getByRole('button', {name: 'increment 2*4'}).click();
  await expect(page.getByText('value=8')).toBeVisible();

  await page.getByRole('button', {name: 'increment 2*10'}).click();
  await expect(page.getByText('value=28')).toBeVisible();
});
