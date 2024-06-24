import {test, expect} from '@playwright/test';

test('test input interactivity works', async ({page}) => {
  await page.goto('/components/input/e2e/input_app');
  await page.getByLabel('Basic input').fill('hi');
  expect(await page.getByText('hi').textContent()).toEqual('hi');
  await page.getByLabel('Basic input').press('Enter');
  expect(await page.getByText('boo').textContent()).toEqual('boo');
});

test('test input on_blur works', async ({page}) => {
  await page.goto('/components/input/e2e/input_blur_app');

  // Fill in input and then click button and make sure values match
  await page.getByLabel('Input').click();
  await page.getByLabel('Input').fill('abc');
  await page.getByRole('button', {name: 'button'}).click();
  await expect(page.getByText('Input: abc')).toBeVisible();
  await expect(
    page.getByText('input_value_when_button_clicked: abc'),
  ).toBeVisible();

  // Same with textarea:
  await page.getByLabel('Regular textarea').click();
  await page.getByLabel('Regular textarea').fill('123');
  await page.getByRole('button', {name: 'button'}).click();
  await expect(page.getByText('Input: 123')).toBeVisible();
  await expect(
    page.getByText('input_value_when_button_clicked: 123'),
  ).toBeVisible();

  // Same with native textarea:
  await page.getByRole('textbox').nth(2).click();
  await page.getByRole('textbox').nth(2).fill('second_textarea');
  await page.getByRole('button', {name: 'button'}).click();
  await expect(page.getByText('Input: second_textarea')).toBeVisible();
  await expect(
    page.getByText('input_value_when_button_clicked: second_textarea'),
  ).toBeVisible();
});
