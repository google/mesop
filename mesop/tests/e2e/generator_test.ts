import {test, expect} from '@playwright/test';

test('generator', async ({page}) => {
  await page.goto('/generator');
  await page.getByRole('button', {name: 'click'}).click();
  // Asserting that some of the text has been yielded.
  // We don't assert the first chunk "foo" to avoid a race condition.
  // The last chunk is delayed by 10 seconds so the chance of a race
  // condition should be low.
  expect(await page.getByText('foobar').textContent()).toEqual('foobar');
});
