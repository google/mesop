import {test, expect} from '@playwright/test';

test('single selection', async ({page}) => {
  await page.goto('/components/select/e2e/select_app');
  await page.getByRole('combobox').click();
  await page.getByRole('option', {name: 'label 2'}).click();
  await expect(page.getByText('Selected value: value2')).toBeAttached();
  await expect(page.getByLabel('label').getByText('label 2')).toBeAttached();

  await page.getByRole('combobox').click();
  await page.getByRole('option', {name: 'label 3'}).click();
  await expect(page.getByText('Selected value: value3')).toBeAttached();
  await expect(page.getByLabel('label').getByText('label 3')).toBeAttached();
});

test('multiple selection', async ({page}) => {
  await page.goto('/components/select/e2e/select_app_multiple');
  await page.getByLabel('Select').click();

  await page.getByRole('option', {name: 'label 2'}).click();
  await expect(
    page.getByText('Selected values: value1, value2, value3'),
  ).toBeAttached();
  await expect(page.getByText('label 1, label 2, label 3')).toBeAttached();

  await page.getByRole('option', {name: 'label 1'}).click();

  await expect(
    page.getByText('Selected values: value2, value3'),
  ).toBeAttached();
  await expect(page.getByText('label 2, label 3')).toBeAttached();
});
