import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/button_toggle/e2e/button_toggle_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
