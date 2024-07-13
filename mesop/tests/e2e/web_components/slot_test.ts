import {test, expect, Page} from '@playwright/test';

test.describe(() => {
  // All tests in this describe group will get 2 retry attempts.
  test.describe.configure({retries: 2});
  test('web components - slot', async ({page}) => {
    await page.goto('http://localhost:32123/web_component/slot/slot_app');
    // Make sure the page has loaded:
    expect(page.getByRole('button', {name: 'Decrement'})).toBeVisible();

    assertValue(10);
    await page.getByRole('button', {name: 'increment'}).click();
    assertValue(11);
    await page.getByRole('button', {name: 'increment'}).click();
    assertValue(12);
    await page.getByRole('button', {name: 'Decrement'}).click();
    assertValue(11);
    await page.getByRole('button', {name: 'Decrement'}).click();
    assertValue(10);

    async function assertValue(value: number) {
      // Check that the outer component is displaying the right value.
      expect(
        await page
          .locator('div')
          .filter({hasText: `Value: ${value} increment Start of`})
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
});
