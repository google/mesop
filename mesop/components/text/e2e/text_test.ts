import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/text/e2e/text_app');
  expect(await page.getByText('H1: Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
