import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/icon/e2e/icon_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
