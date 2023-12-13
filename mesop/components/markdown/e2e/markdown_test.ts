import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/markdown/e2e/markdown_app');
  expect(
    await page.getByText('Sample Markdown Document').textContent(),
  ).toContain('Sample Markdown Document');
});
