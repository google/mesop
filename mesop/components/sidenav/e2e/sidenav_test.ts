import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/sidenav/e2e/sidenav_app');
  expect(await page.getByText('Inside sidenav').textContent()).toContain(
    'Inside sidenav',
  );
});
