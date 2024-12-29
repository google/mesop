import {test, expect} from '@playwright/test';

test('Complex slots', async ({page}) => {
  await page.goto('/testing/complex_slots');

  const header = await page.locator(
    "//component-renderer[*[1][self::component-renderer]/mesop-text/div[text()='---Header Start---']]",
  );
  const firstHeaderButton = await header
    .nth(0)
    .locator(
      "//component-renderer/mesop-expansion-panel//mat-panel-title[contains(@class, 'mat-expansion-panel-header-title') and contains(text(), 'Header Outer')]",
    );
  const firstFooterButton = await header
    .nth(0)
    .locator(
      "//component-renderer/mesop-expansion-panel//mat-panel-title[contains(@class, 'mat-expansion-panel-header-title') and contains(text(), 'Footer Outer')]",
    );
  const secondHeaderButton = await header
    .nth(1)
    .locator(
      "//component-renderer/mesop-expansion-panel//mat-panel-title[contains(@class, 'mat-expansion-panel-header-title') and contains(text(), 'Header Inner')]",
    );
  const secondFooterButton = await header
    .nth(1)
    .locator(
      "//component-renderer/mesop-expansion-panel//mat-panel-title[contains(@class, 'mat-expansion-panel-header-title') and contains(text(), 'Footer Inner')]",
    );
  await expect(firstHeaderButton).toBeVisible();
  await expect(firstFooterButton).toBeVisible();
  await expect(secondHeaderButton).not.toBeVisible();
  await expect(secondFooterButton).not.toBeVisible();

  await firstHeaderButton.click();

  await expect(secondHeaderButton).toBeVisible();
  await expect(secondFooterButton).toBeVisible();

  const headerButtonInner = await page.getByText('Header Inner Button');
  expect(headerButtonInner).not.toBeVisible();
  const footerButtonInner = await page.getByText('Footer Inner Button');
  expect(footerButtonInner).not.toBeVisible();

  await secondHeaderButton.click();
  await secondFooterButton.click();

  expect(footerButtonInner).toBeVisible();
  expect(headerButtonInner).toBeVisible();
});
