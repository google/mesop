import {test, expect} from '@playwright/test';

test('web components - slot', async ({page}) => {
  await page.goto('/web_component/slot/slot_app');

  // Make sure the page has loaded:
  expect(page.getByRole('button', {name: 'Decrement'})).toBeVisible();

  await assertValue(10);
  await page.getByRole('button', {name: 'increment'}).click();
  await assertValue(11);
  await page.getByRole('button', {name: 'increment'}).click();
  await assertValue(12);
  await page.getByRole('button', {name: 'Decrement'}).click();
  await assertValue(11);
  await page.getByRole('button', {name: 'Decrement'}).click();
  await assertValue(10);

  async function assertValue(value: number) {
    // Check that the outer component is displaying the right value.
    expect(
      await page
        .locator('#outer-value')
        .filter({hasText: `Value: ${value}`})
        .textContent(),
    ).toContain(value.toString());

    // Check that the inner component is displaying the right value.
    expect(
      await page
        .locator('slot-counter-component')
        .getByText('Value:')
        .textContent(),
    ).toContain(value.toString());
  }
});

test('web components - slot child reconciliation', async ({page}) => {
  await page.goto('/web_component/slot/slot_app');
  await page.getByLabel('input slot').click();
  await page.getByLabel('input slot').fill('abc');

  await page.locator('slot-counter-component').getByRole('textbox').click();
  await page.locator('slot-counter-component').getByRole('textbox').fill('def');

  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByRole('button', {name: 'add checkbox slot'}).click();

  await page.getByRole('checkbox').click();

  // Assertions
  await expect(page.getByRole('checkbox')).toBeChecked();
  await expect(page.getByText('Checked? true')).toBeVisible();
  expect(await page.getByLabel('input slot').inputValue()).toEqual('abc');
  expect(
    await page
      .locator('slot-counter-component')
      .getByRole('textbox')
      .inputValue(),
  ).toEqual('def');
});
