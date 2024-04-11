import {test, expect} from '@playwright/test';

test('Chat UI can send messages and display responses', async ({page}) => {
  // Increase the default time out since this test is slow and has multiple steps.
  test.setTimeout(30000);

  await page.goto('/chat');

  // Test that we can send a message.
  await page.locator('//input').fill('Lorem ipsum');
  // Need to wait for the input state to be saved before clicking.
  await page.waitForTimeout(2000);
  await page.getByRole('button', {name: 'Send prompt'}).click();
  await expect(
    page.getByRole('button', {name: 'Processing prompt...'}),
  ).toBeAttached({timeout: 3000});
  await expect(page.locator('//input')).toHaveValue('');
  expect(page.locator('//div[text()="Lorem ipsum"]')).toHaveCount(1);
  await expect(page.locator('//div[text()="Lorem Ipsum Bot"]')).toHaveCount(1);
  // Since the text is random, we just check that some text is displayed.
  await expect(page.locator('//mesop-markdown')).toContainText(/[\w]+/);

  // The chat example's transform function has a fake delay per line. The number of
  // lines are also randomly. So we need a longer delay.
  await expect(page.getByRole('button', {name: 'Send prompt'})).toBeAttached({
    timeout: 10000,
  });

  // Test that we can send more than one message.
  await page.locator('//input').fill('Dolor sit amet');
  // Need to wait for the input state to be saved before clicking.
  await page.waitForTimeout(2000);
  await page.getByRole('button', {name: 'Send prompt'}).click();
  await expect(
    page.getByRole('button', {name: 'Processing prompt...'}),
  ).toBeAttached({timeout: 3000});
  await expect(page.locator('//input')).toHaveValue('');
  await expect(page.locator('//div[text()="Dolor sit amet"]')).toHaveCount(1);
  await expect(page.locator('//div[text()="Lorem Ipsum Bot"]')).toHaveCount(2);
  // Since the text is random, we just check that some text is displayed.
  await expect(page.locator('//mesop-markdown')).toContainText([
    /[\w]+/,
    /[\w]+/,
  ]);
});
