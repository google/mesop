import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/progress_spinner/e2e/progress_spinner_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
