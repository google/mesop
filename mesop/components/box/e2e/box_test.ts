import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/box/e2e/box_app');
  expect(await page.getByText('hi1').textContent()).toContain('hi1');
  expect(await page.getByText('hi2').textContent()).toContain('hi2');
});
