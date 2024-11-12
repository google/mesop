import {test, expect} from '@playwright/test';

test('browser navigation - back and forward (triggers onload)', async ({
  page,
}) => {
  await page.goto('/browser_navigation_on_load/page1');
  await expect(page.getByText('page1')).toBeVisible();
  await expect(page.getByText('onload ran 1 times')).toBeVisible();

  // Trigger a navigation.
  await page.getByRole('button', {name: 'navigate'}).click();

  await expect(page.getByText('page2')).toBeVisible();
  await expect(page.getByText('onload ran 1 times')).toBeVisible();

  // Go back to page 1
  await page.goBack();
  await expect(page.getByText('page1')).toBeVisible();
  await expect(page.getByText('onload ran 2 times')).toBeVisible();

  // Go forward to page 2
  await page.goForward();
  await expect(page.getByText('page2')).toBeVisible();
  await expect(page.getByText('onload ran 2 times')).toBeVisible();
});
