import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/slide_toggle/e2e/slide_toggle_app');
  expect(await page.getByText('Toggled:').textContent()).toContain(
    'Toggled: False',
  );
});
