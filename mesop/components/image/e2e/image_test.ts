import {test} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/image/e2e/image_app');

  await page.waitForSelector('img', {state: 'visible'});
});
