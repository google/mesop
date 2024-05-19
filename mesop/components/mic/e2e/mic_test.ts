import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/mic/e2e/mic_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
