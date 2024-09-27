import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/date_range_picker/e2e/date_range_picker_app');
  expect(await page.getByText('Hello, world!').textContent()).toContain(
    'Hello, world!',
  );
});
