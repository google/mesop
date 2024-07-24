import {test, expect} from '@playwright/test';

test('Chat UI can send messages and display responses', async ({page}) => {
  // Increase the default time out since this test is slow and has multiple steps.
  test.setTimeout(30000);

  await page.goto('/testing/minimal_chat');

  // Test that we can send a message.
  await page.locator('//input').fill('Lorem ipsum');
  // Need to wait for the input state to be saved before clicking.
  await page.waitForTimeout(2000);
  await page.getByRole('button').filter({hasText: 'send'}).click();
  await expect(page.locator('//input')).toHaveValue('');
  expect(page.locator('//div[text()="Lorem ipsum"]')).toHaveCount(1);
  await expect(page.locator('//div[text()="Lorem Ipsum Bot"]')).toHaveCount(1);
  // Since the text is random, we just check that some text is displayed.
  await expect(page.locator('//mesop-markdown')).toContainText(/[\w]+/);

  // The chat example's transform function has a fake delay per line. The number of
  // lines are also randomly. So we need a longer delay.
  await expect(page.getByRole('button').filter({hasText: 'send'})).toBeAttached(
    {
      timeout: 10000,
    },
  );

  // Test that we can send more than one message by pressing "Enter"
  await page.locator('//input').fill('Dolor sit amet');
  // Need to wait for the input state to be saved before submitting.
  await page.waitForTimeout(2000);
  await page.locator('//input').press('Enter');
  await expect(page.locator('//input')).toHaveValue('');
  await expect(page.locator('//div[text()="Dolor sit amet"]')).toHaveCount(1);
  await expect(page.locator('//div[text()="Lorem Ipsum Bot"]')).toHaveCount(2);
  // Since the text is random, we just check that some text is displayed.
  await expect(page.locator('//mesop-markdown')).toContainText([
    /[\w]+/,
    /[\w]+/,
  ]);
});

test('Chat UI toggle dark theme', async ({page}) => {
  await page.goto('/testing/minimal_chat');
  expect(await page.evaluate(hasDarkTheme)).toBeFalsy();

  await page.locator('button').filter({hasText: 'dark_mode'}).click();

  // Wait for light mode button to be visible to avoid a race when
  // checking if the page has dark theme enabled.
  const lightModeButton = page
    .locator('button')
    .filter({hasText: 'light_mode'});
  await expect(lightModeButton).toBeVisible();
  expect(await page.evaluate(hasDarkTheme)).toBeTruthy();

  await lightModeButton.click();

  // Wait for the dark mode button to be visible to avoid a race.
  await expect(
    page.locator('button').filter({hasText: 'dark_mode'}),
  ).toBeVisible();
  expect(await page.evaluate(hasDarkTheme)).toBeFalsy();
});

function hasDarkTheme() {
  return document.body.classList.contains('dark-theme');
}
