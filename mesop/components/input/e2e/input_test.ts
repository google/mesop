import {test} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/input/e2e/input_app');
  // TODO: write test.
  // expect(await page.getByText('Hello, world!').textContent()).toContain(
  //   'Hello, world!',
  // );
});
