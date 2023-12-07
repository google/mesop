import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/component_name/e2e/component_name_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
