import {test, expect} from '@playwright/test';

test('set_serialize', async ({page}) => {
  await page.goto('/testing/set_serialize');

  await expect(page.getByText('Set values: []')).toBeAttached();
  await expect(page.getByText('Is set: True')).toBeAttached();

  await page.getByRole('button', {name: 'Init set', exact: true}).click();

  await expect(page.getByText('Set values: [1, 2, 3]')).toBeAttached();
  await expect(page.getByText('Is set: True')).toBeAttached();

  await page.getByRole('button', {name: 'Update set', exact: true}).click();

  await expect(page.getByText('Set values: [1, 2, 3, 4]')).toBeAttached();
  await expect(page.getByText('Is set: True')).toBeAttached();

  await page.getByRole('button', {name: 'Init set', exact: true}).click();

  await expect(page.getByText('Set values: [1, 2, 3]')).toBeAttached();
  await expect(page.getByText('Is set: True')).toBeAttached();
});
