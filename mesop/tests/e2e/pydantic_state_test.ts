import {test, expect} from '@playwright/test';

test('pydantic state is serialized and deserialized properly', async ({
  page,
}) => {
  await page.goto('/pydantic_state');

  await expect(page.getByText('Name: world')).toBeVisible();
  await expect(page.getByText('Counter: 0')).toBeVisible();
  await page.getByRole('button', {name: 'Increment Counter'}).click();
  await expect(page.getByText('Counter: 1')).toBeVisible();
  // await page.getByRole('button', {name: 'Increment Counter'}).click();
  // await expect(page.getByText('Counter: 2')).toBeVisible();
});
