import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/badge/e2e/badge_app');
  expect(await page.getByText('1').textContent()).toContain('1');
});
