import {test, expect} from '@playwright/test';

test('test box', async ({page}) => {
  await page.goto('/components/box/e2e/box_app');
  await page.getByText('outer-box').click();
  await expect(page.getByText('Outer counter: 1')).toBeVisible();
  await page.getByText('inner-box').click();
  await expect(page.getByText('Outer counter: 2')).toBeVisible();
  await expect(page.getByText('Inner counter: 1')).toBeVisible();
});
