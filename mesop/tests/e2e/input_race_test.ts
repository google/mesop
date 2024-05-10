import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  // This test is relatively slower because there's a few
  // sequential steps.
  test.setTimeout(30000);

  await page.goto('/input_race');

  // Trigger an initial user event.
  await page.getByLabel('Input a').fill('1');
  // Trigger two user events "2", "3" which will
  // probably get queued.
  await page.getByLabel('Input a').pressSequentially('23');
  // Trigger a user event with the same handler function
  // but different key to check that this edge case is handled.
  await page.getByLabel('Input b').fill('45');
  // Trigger a click user event to save the value of Input a.
  await page.getByRole('button', {name: 'Click'}).click();

  // Assert that the text for each field is as expected.
  await expectTextExists('State.input_a: 123');
  await expectTextExists('State.input_b: 45');
  await expectTextExists('State.input_on_click: 123');

  async function expectTextExists(text: string) {
    expect(await page.getByText(text).textContent()).toEqual(text);
  }
});
