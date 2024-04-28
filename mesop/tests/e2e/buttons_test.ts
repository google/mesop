import {test, expect} from '@playwright/test';

test('buttons', async ({page}) => {
  await page.goto('/buttons');
  expect(await page.getByText('0 clicks').textContent()).toEqual('0 clicks');
  await page.getByRole('button', {name: 'primary color button'}).click();
  expect(await page.getByText('1 clicks').textContent()).toEqual('1 clicks');
});
