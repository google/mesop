import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/table/e2e/table_app');

  // Check headers rendered.
  await expect(page.locator(`//th[contains(text(), "NA")]`)).toBeAttached();
  await expect(page.locator(`//th[contains(text(), "Bools")]`)).toBeAttached();
  await expect(page.locator(`//th[contains(text(), "Ints")]`)).toBeAttached();
  await expect(page.locator(`//th[contains(text(), "Floats")]`)).toBeAttached();
  await expect(
    page.locator(`//th[contains(text(), "Strings")]`),
  ).toBeAttached();
  await expect(
    page.locator(`//th[contains(text(), "DateTimes")]`),
  ).toBeAttached();

  // Spot check that expected table values are rendered.
  await expect(
    page.locator(
      `//td[contains(@class, "mat-column-NA") and contains(text(), "<NA>")]`,
    ),
  ).toHaveCount(3);
  await expect(
    page.locator(
      `//td[contains(@class, "mat-column-Bools") and contains(text(), "False")]`,
    ),
  ).toBeAttached();
  await expect(
    page.locator(
      `//td[contains(@class, "mat-column-Ints") and contains(text(), "-55")]`,
    ),
  ).toBeAttached();
  await expect(
    page.locator(
      `//td[contains(@class, "mat-column-Floats") and contains(text(), "4.5")]`,
    ),
  ).toBeAttached();
  await expect(
    page.locator(
      `//td[contains(@class, "mat-column-Strings") and contains(text(), "World")]`,
    ),
  ).toBeAttached();
  await expect(
    page.locator(
      `//td[contains(@class, "mat-column-DateTimes") and contains(text(), "2018-03-10 00:00:00")]`,
    ),
  ).toBeAttached();

  // Check expected number of rows rendered.
  await expect(
    page.locator(`//td[contains(@class, "mat-column-NA")]`),
  ).toHaveCount(3);
  await expect(
    page.locator(`//td[contains(@class, "mat-column-Bools")]`),
  ).toHaveCount(3);
  await expect(
    page.locator(`//td[contains(@class, "mat-column-Ints")]`),
  ).toHaveCount(3);
  await expect(
    page.locator(`//td[contains(@class, "mat-column-Floats")]`),
  ).toHaveCount(3);
  await expect(
    page.locator(`//td[contains(@class, "mat-column-Strings")]`),
  ).toHaveCount(3);
  await expect(
    page.locator(`//td[contains(@class, "mat-column-DateTimes")]`),
  ).toHaveCount(3);
});
