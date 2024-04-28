import {test, expect} from '@playwright/test';

test('navigation', async ({page}) => {
  await page.goto('/');

  // Check the text that we're on the home page.
  expect(
    await page.getByRole('heading', {name: 'Welcome'}).textContent(),
  ).toEqual('Welcome');

  // Trigger a navigation by clicking on the nav menu button.
  await page.getByRole('button', {name: 'Playground', exact: true}).click();

  // Check the text has changed which means navigation succeeded.
  expect(await page.getByText('Playground Page').textContent()).toEqual(
    'Playground Page',
  );
});
