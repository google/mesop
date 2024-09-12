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

test('renders code copy', async ({browser}) => {
  // Need permission to read clipboard
  const context = await browser.newContext();
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);

  const page = await context.newPage();
  await page.goto('/components/markdown/e2e/markdown_app');

  // Can copy text
  await page.locator('.code-block').nth(0).hover();
  await page.locator('//a[contains(@class, "code-copy-0")]').click();
  let clipboardContent = await page.evaluate(async () => {
    return await navigator.clipboard.readText();
  });
  expect(clipboardContent).toBe('hello');

  // Can copy text if there are multiple code blocks
  await page.locator('.code-block').nth(1).hover();
  await page.locator('//a[contains(@class, "code-copy-1")]').click();
  clipboardContent = await page.evaluate(async () => {
    return await navigator.clipboard.readText();
  });
  expect(clipboardContent).toContain('print("Hello, World 1!")');

  // Can copy text if markdown is updated
  await page.getByText('Updated markdown').click();
  await page.waitForTimeout(1000);
  await expect(async () => {
    await page.locator('.code-block').nth(0).hover();
    await page.locator('//a[contains(@class, "code-copy-0")]').click();
  }).toPass({timeout: 5000});
  clipboardContent = await page.evaluate(async () => {
    return await navigator.clipboard.readText();
  });
  expect(clipboardContent).toContain('print("Hello, World 3!")');
});
