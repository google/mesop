import {test, expect} from '@playwright/test';

test('test input interactivity works', async ({page}) => {
  await page.goto('/components/input/e2e/input_app');
  await page.getByLabel('Basic input').fill('hi');
  expect(await page.getByText('hi').textContent()).toEqual('hi');
  await page.getByLabel('Basic input').press('Enter');
  expect(await page.getByText('boo').textContent()).toEqual('boo');
});
