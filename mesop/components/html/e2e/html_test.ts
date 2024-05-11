import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/html/e2e/html_app');
  // mesop is the HTML link so we're checking that it's rendered.
  expect(await page.getByText('Custom HTML').textContent()).toContain(
    'mesoplink',
  );
});
