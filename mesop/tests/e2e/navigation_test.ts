import {test, expect} from '@playwright/test';

test('navigation', async ({page}) => {
  await page.goto('/index');

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

test('navigation inside generator handler function', async ({page}) => {
  await page.goto('/navigate_advanced/page1');

  // Check the text that we're on the first page.
  expect(await page.getByText('page1').textContent()).toEqual('page1');

  // Trigger a navigation.
  await page.getByRole('button', {name: 'navigate', exact: true}).click();

  // Check the text has changed which means navigation succeeded.
  expect(await page.getByText('page2').textContent()).toEqual('page2');
});

test('navigation absolute - https', async ({page}) => {
  await page.goto('/navigate_absolute');

  // Trigger a navigation.
  await page.getByRole('button', {name: 'navigate https', exact: true}).click();

  // Wait for navigation to complete
  await expect(page).toHaveURL('https://www.google.com/');
});

test('navigation absolute - http', async ({page}) => {
  await page.goto('/navigate_absolute');

  // Trigger a navigation.
  await page.getByRole('button', {name: 'navigate http', exact: true}).click();

  // Wait for navigation to complete
  await expect(page).toHaveURL('http://example.com/');
});

test('navigation yield', async ({page}) => {
  await page.goto('/navigate_absolute');

  // Trigger a navigation.
  await page.getByRole('button', {name: 'navigate yield', exact: true}).click();

  // Wait for navigation to complete
  await expect(page).toHaveURL('https://www.google.com/');
});
