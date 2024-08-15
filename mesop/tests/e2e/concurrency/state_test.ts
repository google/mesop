/**
 * The purpose of this test is to ensure that sessions have proper
 * state isolation, particularly under high concurrency.
 *
 * Run test as:
 * yarn playwright test mesop/tests/e2e/concurrency/state_test.ts --repeat-each=48 --workers=16
 */
import {test, expect} from '@playwright/test';

test('state updates correctly', async ({page}) => {
  await page.goto('/concurrency_state');
  const randomString = generateRandomString(16);
  await page.getByLabel('State input').fill(randomString);
  await expect(page.getByText(`Input: ${randomString}`)).toBeVisible({
    timeout: 15000,
  });
});

function generateRandomString(length: number) {
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}
