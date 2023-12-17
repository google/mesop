import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/divider/e2e/divider_app');
  expect(await page.textContent('body')).toContain('beforeafter');
});
