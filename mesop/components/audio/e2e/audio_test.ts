import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/audio/e2e/audio_app');
  const selector = await page.waitForSelector('audio');
  expect(selector).toBeTruthy();
});
