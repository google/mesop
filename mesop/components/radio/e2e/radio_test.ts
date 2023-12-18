import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/radio/e2e/radio_app');
  expect(
    await page.getByText('Selected radio value: ').textContent(),
  ).toContain('Selected radio value: 2');

  await page.getByRole('radio', {name: 'Hello', exact: true}).check();
  expect(
    await page.getByText('Selected radio value: 1').textContent(),
  ).toContain('Selected radio value: 1');
});
