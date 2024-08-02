import {test, expect} from '@playwright/test';

const isFocused = (selector: string) => {
  const element = document.querySelector(selector);
  return document.activeElement === element;
};

test('focus autocomplete', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Autocomplete'}).click();
  await expect(
    await page.evaluate(isFocused, 'input[aria-controls="mat-autocomplete-0"]'),
  ).toBe(true);
});

test('focus checkbox', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Checkbox'}).click();
  await expect(await page.evaluate(isFocused, 'input[type="checkbox"]')).toBe(
    true,
  );
});

test('focus text input', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Input'}).click();
  await expect(await page.evaluate(isFocused, 'input[id="mat-input-1"]')).toBe(
    true,
  );
});

test('focus link', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Link'}).click();
  await expect(await page.evaluate(isFocused, 'a')).toBe(true);
});

test('focus radio', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Radio'}).click();
  await expect(
    await page.evaluate(isFocused, 'input[name="mat-radio-group-0"]'),
  ).toBe(true);
});

test('focus select', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Select'}).click();
  await expect(
    await page.evaluate(isFocused, 'mat-select[id="mat-select-2"]'),
  ).toBe(true);
});

test('focus slider', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Slider'}).click();
  await expect(await page.evaluate(isFocused, 'input[type="range"]')).toBe(
    true,
  );
});

test('focus slider toggle', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Slide Toggle'}).click();
  await expect(await page.evaluate(isFocused, 'button[role="switch"]')).toBe(
    true,
  );
});

test('focus textarea', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Textarea'}).click();
  await expect(await page.evaluate(isFocused, 'textarea')).toBe(true);
});

test('focus uploader', async ({page}) => {
  await page.goto('/focus_component');
  await page.locator('//mat-select[@id="mat-select-0"]').click();
  await page.getByRole('option', {name: 'Uploader'}).click();
  await expect(await page.evaluate(isFocused, 'mesop-uploader button')).toBe(
    true,
  );
});
