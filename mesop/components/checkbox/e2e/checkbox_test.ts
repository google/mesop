import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/checkbox/e2e/checkbox_app');
  expect(await page.getByText('is checked').textContent()).toContain(
    'is checked',
  );

  await page.getByRole('checkbox').uncheck();

  expect(await page.getByText('is not checked').textContent()).toContain(
    'is not checked',
  );
});
