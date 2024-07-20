import {test, expect} from '@playwright/test';

test('open same tab', async ({page}) => {
  await page.goto('/components/link/e2e/link_app');

  await page.getByRole('link', {name: 'Open in same tab'}).click();
  await expect(page).toHaveURL('https://www.google.com/');
});

test('open new tab', async ({page}) => {
  await page.goto('/components/link/e2e/link_app');

  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('link', {name: 'Open in new tab'}).click();
  const page1 = await page1Promise;
  await expect(page1).toHaveURL('https://www.google.com/');
});
