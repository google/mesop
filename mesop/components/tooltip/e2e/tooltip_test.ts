import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/tooltip/e2e/tooltip_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
