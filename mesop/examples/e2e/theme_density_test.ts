import {test, expect} from '@playwright/test';

test('theme density', async ({page}) => {
  await page.goto('/testing/theme_density');

  // Open select dropdown:
  await page.locator('div').filter({hasText: 'Density'}).first().click();
  // Select -1 option:
  await page.getByRole('option', {name: '-1'}).click();
  expect(await page.evaluate(hasThemeDensity, -1)).toEqual(true);

  // Open select dropdown:
  await page.locator('div').filter({hasText: 'Density-'}).first().click();
  // Select -3 option:
  await page.getByRole('option', {name: '-3'}).click();
  expect(await page.evaluate(hasThemeDensity, -1)).toEqual(false);
  expect(await page.evaluate(hasThemeDensity, -3)).toEqual(true);
});

function hasThemeDensity(density: number) {
  return document.body.classList.contains('theme-density-' + density);
}
