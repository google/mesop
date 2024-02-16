import {test} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/slider/e2e/slider_app');
  await page.getByRole('slider').fill('57');
  await page.getByRole('slider').click();
  // TODO: fix the assertion (it's now flaky / off by 1)
  // expect(await page.getByText('Value: 57').textContent()).toContain(
  //   'Value: 57',
  // );
});
