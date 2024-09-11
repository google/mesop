import {test, expect} from '@playwright/test';

test('test input interactivity works', async ({page}) => {
  await page.goto('/components/input/e2e/input_app');
  await page.getByLabel('Basic input').fill('hi');
  expect(await page.getByText('hi').textContent()).toEqual('hi');
});

test('test input on_enter works', async ({page}) => {
  await page.goto('/components/input/e2e/input_app');
  await page.getByLabel('Input (on_enter)').fill('typing and then enter');
  await page.getByLabel('Input (on_enter)').press('Enter');
  await expect(page.getByText('typing and then enter')).toBeVisible();
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

// TODO: unskip this test once the flakiness is fixed
test.skip('test textarea shortcuts', async ({page}) => {
  await page.goto('/components/input/e2e/textarea_shortcut_app');
  const textbox = page.getByLabel('Textarea');
  await textbox.fill('hi');
  await page.keyboard.press('Enter');
  await expect(await page.getByText('Submitted: hi')).toBeVisible();

  await page.keyboard.down('Shift');
  await page.keyboard.press('Enter');
  await page.keyboard.up('Shift');
  await expect(await page.getByText('Submitted: hi')).toBeVisible();

  await textbox.pressSequentially('hi');
  await page.keyboard.press('Enter');
  await expect(async () => {
    await expect(await page.getByText('Submitted: hi hi')).toBeVisible();
  }).toPass({timeout: 5000});
  await page.keyboard.down('Meta');
  await page.keyboard.press('s');
  await page.keyboard.up('Meta');
  await expect(
    await page.getByText(
      "Shortcut: Shortcut(key='S', shift=False, ctrl=False, alt=False, meta=True)",
    ),
  ).toBeVisible();

  await page.keyboard.down('Control');
  await page.keyboard.down('Alt');
  await page.keyboard.press('Enter');
  await page.keyboard.up('Control');
  await page.keyboard.up('Alt');
  await expect(
    await page.getByText(
      "Shortcut: Shortcut(key='Enter', shift=False, ctrl=True, alt=True, meta=False)",
    ),
  ).toBeVisible();

  await page.keyboard.press('Escape');
  await expect(
    await page.getByText(
      "Shortcut: Shortcut(key='escape', shift=False, ctrl=False, alt=False, meta=False)",
    ),
  ).toBeVisible();
});

// TODO: unskip this test once the flakiness is fixed
test.skip('test native textarea shortcuts', async ({page}) => {
  await page.goto('/components/input/e2e/textarea_shortcut_app');
  const textbox = page.getByPlaceholder('Native textarea');

  await textbox.fill('hi');
  await page.keyboard.press('Enter');
  await expect(await page.getByText('Submitted: hi')).toBeVisible();

  await page.keyboard.down('Shift');
  await page.keyboard.press('Enter');
  await page.keyboard.up('Shift');
  await expect(await page.getByText('Submitted: hi')).toBeVisible();

  await textbox.pressSequentially('hi');
  await page.keyboard.press('Enter');
  await expect(await page.getByText('Submitted: hi hi')).toBeVisible();

  await page.keyboard.down('Meta');
  await page.keyboard.press('s');
  await page.keyboard.up('Meta');
  await expect(
    await page.getByText(
      "Shortcut: Shortcut(key='S', shift=False, ctrl=False, alt=False, meta=True)",
    ),
  ).toBeVisible();

  await page.keyboard.down('Control');
  await page.keyboard.down('Alt');
  await page.keyboard.press('Enter');
  await page.keyboard.up('Control');
  await page.keyboard.up('Alt');
  await expect(
    await page.getByText(
      "Shortcut: Shortcut(key='Enter', shift=False, ctrl=True, alt=True, meta=False)",
    ),
  ).toBeVisible();

  await page.keyboard.press('Escape');
  await expect(
    await page.getByText(
      "Shortcut: Shortcut(key='escape', shift=False, ctrl=False, alt=False, meta=False)",
    ),
  ).toBeVisible();
});
