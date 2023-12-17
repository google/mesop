import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/progress_bar/e2e/progress_bar_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
