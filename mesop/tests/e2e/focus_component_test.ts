import {Page, test, expect} from '@playwright/test';

const checkIsFocused = (selector: string) => {
  const element = document.querySelector(selector);
  return document.activeElement === element;
};

const expectIsFocused = async (page: Page, selector: string) => {
  return await expect(async () => {
    const isFocused = await page.evaluate(checkIsFocused, selector);
    expect(isFocused).toBe(true);
  }).toPass({timeout: 5000});
};

test('focus autocomplete', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Autocomplete'}).click();
  await expectIsFocused(page, 'input[aria-controls="mat-autocomplete-0"]');
});

test('focus checkbox', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Checkbox'}).click();
  await expectIsFocused(page, 'input[type="checkbox"]');
});

test('focus text input', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Input'}).click();
  await expectIsFocused(page, 'input[id="mat-input-1"]');
});

test('focus link', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Link'}).click();
  await expectIsFocused(page, 'a');
});

test('focus radio', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Radio'}).click();
  await expectIsFocused(page, 'input[name="mat-radio-group-0"]');
});

test('focus select', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Select'}).click();
  await expectIsFocused(page, 'mat-select[id="mat-select-2"]');
});

test('focus slider', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Slider'}).click();
  await expectIsFocused(page, 'input[type="range"]');
});

test('focus slider toggle', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Slide Toggle'}).click();
  await expectIsFocused(page, 'button[role="switch"]');
});

test('focus textarea', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Textarea'}).click();
  await expectIsFocused(page, 'textarea');
});

test('focus uploader', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Uploader'}).click();
  await expectIsFocused(page, 'mesop-uploader button');
});
