import {test, expect} from '@playwright/test';

test('event handler error message is shown', async ({page}) => {
  await page.goto('/event_handler_error');

  // Regular event handler
  await page.getByRole('button', {name: 'Regular event handler'}).click();
  await expect(
    page.getByText('Error in on_click.', {exact: true}),
  ).toBeVisible();
  await page.locator('button').filter({hasText: 'close'}).click();

  // Generator event handler
  await page
    .getByRole('button', {name: 'Generator event handler', exact: true})
    .click();
  await expect(
    page.getByText('Error in on_click_generator.', {exact: true}),
  ).toBeVisible();
  await page.locator('button').filter({hasText: 'close'}).click();

  // Yield from event handler
  await page.getByRole('button', {name: 'Yield from event handler'}).click();
  await expect(
    page.getByText('Error in a_generator.', {exact: true}),
  ).toBeVisible();
  await page.locator('button').filter({hasText: 'close'}).click();

  // Async generator event handler
  await page
    .getByRole('button', {name: 'Async generator event handler'})
    .click();
  await expect(
    page.getByText('Error in on_click_async_generator.', {exact: true}),
  ).toBeVisible();
  await page.locator('button').filter({hasText: 'close'}).click();
});
