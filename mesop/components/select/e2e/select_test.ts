import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/select/e2e/select_app');
  await page.getByLabel('Select').click();
  await page.getByRole('option', {name: 'label 2'}).click();

  expect(
    await page.getByText('Selected value: value2').textContent(),
  ).toContain('Selected value: value2');
});
