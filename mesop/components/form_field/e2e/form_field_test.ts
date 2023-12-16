import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/form_field/e2e/form_field_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
