import {test, expect} from '@playwright/test';

test('test conditional event handler', async ({page}) => {
  await page.goto('/testing/conditional_event_handler');
  await page.goto('http://localhost:32123/testing/conditional_event_handler');
  await page.getByLabel('first checkbox').check();
  await page.getByLabel('second checkbox').check();
  expect(
    await page.getByText('second checkbox has been').textContent(),
  ).toEqual('second checkbox has been checked');
});
