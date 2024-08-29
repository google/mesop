import {test, expect} from '@playwright/test';

test('viewport_size', async ({page}) => {
  await page.goto('/viewport_size');
  await page.setViewportSize({width: 400, height: 300});
  // For the following assertions, make sure the width has updated so that
  // there isn't a race condition.
  expect(await page.getByText('viewport_size width=400').textContent()).toEqual(
    'viewport_size width=400 height=300',
  );
  await page.setViewportSize({width: 500, height: 200});
  expect(await page.getByText('viewport_size width=500').textContent()).toEqual(
    'viewport_size width=500 height=200',
  );
});

test('viewport_size - works for any user event', async ({page}) => {
  await page.goto('/viewport_size');
  expect(await page.getByText('Count:').textContent()).toEqual('Count: 0');
  await page.getByRole('button', {name: 'on_click should work'}).click();
  // Make sure counter has been incremented to know that user event has been processed.
  expect(await page.getByText('Count: 1').textContent()).toEqual('Count: 1');
});
