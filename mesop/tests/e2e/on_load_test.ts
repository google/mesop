import {test, expect, Page} from '@playwright/test';

test('on_load (non-generator)', async ({page}) => {
  await page.goto('/on_load');

  await assertPageHasText(page, "/on_load ['a', 'b']");
});

test('on_load (generator)', async ({page}) => {
  await page.goto('/on_load_generator');

  await assertGeneratorPage(page);
});

test('on_load - navigate triggers on load handler', async ({page}) => {
  await page.goto('/on_load');

  await page
    .getByRole('button', {name: 'navigate to /on_load_generator'})
    .click();

  await assertGeneratorPage(page);
});

async function assertGeneratorPage(page: Page) {
  // Initial flush:
  await assertPageHasText(page, '<init>');

  // 2nd flush:
  await assertPageHasText(page, '<not-default>');
  await assertPageHasText(page, "/on_load_generator ['a']");
  expect(
    await page
      .locator('[data-key="replaced values"]')
      .locator('..')
      .textContent(),
  ).toEqual('123');

  // 3rd flush:
  await assertPageHasText(page, "/on_load_generator ['a', 'b']");
  expect(
    await page
      .locator('[data-key="replaced values"]')
      .locator('..')
      .textContent(),
  ).toEqual('456');
}

async function assertPageHasText(page: Page, text: string) {
  expect(await page.getByText(text).textContent()).toEqual(text);
}
