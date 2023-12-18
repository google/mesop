import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/slider/e2e/slider_app');
  await page.getByRole('slider').fill('57');
  await page.getByRole('slider').click();
  expect(await page.getByText('Value: 57').textContent()).toContain(
    'Value: 57',
  );
});
