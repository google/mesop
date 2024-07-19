import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/link/e2e/link_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
