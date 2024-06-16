import {test, expect} from '@playwright/test';

test('web components - slot', async ({page}) => {
  await page.goto('http://localhost:32123/web_component/slot/slot_app');
  expect(
    await page
      .locator('div')
      .filter({hasText: 'Value: 10 increment Start of'})
      .locator('span')
      .isVisible(),
  ).toEqual(true);
  expect(page.getByRole('button', {name: 'Decrement'})).toBeVisible();
  await new Promise((r) => setTimeout(r, 3000));
  expect(await page.locator('body').textContent()).toEqual('...');
  // await page.goto('http://localhost:32123/web_component/slot/slot_app');
  await page
    .locator('div')
    .filter({hasText: 'Value: 10 increment Start of'})
    .locator('span')
    .click();
  await page.locator('slot-counter-component').getByText('Value:').click();
  await page.getByRole('button', {name: 'increment'}).click();
  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByRole('button', {name: 'Decrement'}).click();

  // expect(await page.getByText('Value: ').textContent()).toEqual('Value: 10');
  // await page.getByRole('button', {name: 'Decrement'}).click();
  // await page.getByText('Value: 9').textContent();
  // await page.getByRole('button', {name: 'Decrement'}).click();
  // await page.getByText('Value: 8').textContent();
});
