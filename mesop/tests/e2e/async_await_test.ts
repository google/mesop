import {test, expect} from '@playwright/test';

test('async await', async ({page}) => {
  await page.goto('/async_await');
  await page.getByRole('button', {name: 'async with yield'}).click();
  await expect(page.getByText('val1=<async_value>')).toBeVisible({
    // Intentionally set timeout at 3 seconds to make sure the
    // async work is happening in parallel.
    timeout: 3000,
  });
  expect(await page.getByText('val2=').textContent()).toEqual(
    'val2=<async_value>',
  );
});

test('async await no yield', async ({page}) => {
  await page.goto('/async_await');
  await page.getByRole('button', {name: 'async without yield'}).click();
  await expect(page.getByText('val1=<async_value>')).toBeVisible({
    // Intentionally set timeout at 3 seconds to make sure the
    // async work is happening in parallel.
    timeout: 3000,
  });
  expect(await page.getByText('val2=').textContent()).toEqual(
    'val2=<async_value>',
  );
});
