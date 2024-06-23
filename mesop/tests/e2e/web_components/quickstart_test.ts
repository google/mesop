import {test, expect} from '@playwright/test';

test('web components - quickstart', async ({page}) => {
  await page.goto('/web_component/quickstart/counter_component_app');
  expect(await page.getByText('Value: ').textContent()).toEqual('Value: 10');
  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByText('Value: 9').textContent();
  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByText('Value: 8').textContent();
});
