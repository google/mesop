import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/markdown/e2e/markdown_app');
  expect(
    await page.getByText('Sample Markdown Document').textContent(),
  ).toContain('Sample Markdown Document');
});

test('renders table markup', async ({page}) => {
  await page.goto('/components/markdown/e2e/markdown_app');

  await expect(
    page.locator(`//table/thead/tr/th[contains(text(), "Header")]`),
  ).toHaveCount(2);

  await expect(
    page.locator(`//table/tbody/tr/td[contains(text(), "Content Cell")]`),
  ).toHaveCount(4);
});
