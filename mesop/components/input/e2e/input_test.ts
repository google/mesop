import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/input/e2e/input_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
