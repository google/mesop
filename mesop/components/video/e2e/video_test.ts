import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/video/e2e/video_app');
  const selector = await page.waitForSelector('video');
  expect(selector).toBeTruthy();
});
