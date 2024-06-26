import {test, expect} from '@playwright/test';

test('dict state is serialized properly', async ({page}) => {
  await page.goto('/dict_state');

  await expect(page.getByText('Checks: dict_items([])')).toBeVisible();
  await page.getByLabel('box1').check();
  await expect(
    page.getByText("Checks: dict_items([('box1', True)])"),
  ).toBeVisible();
  await page.getByLabel('box2').check();
  await expect(
    page.getByText("Checks: dict_items([('box1', True), ('box2', True)])"),
  ).toBeVisible();
  await page.getByLabel('box1').uncheck();
  await expect(
    page.getByText("Checks: dict_items([('box1', False), ('box2', True)])"),
  ).toBeVisible();
});
