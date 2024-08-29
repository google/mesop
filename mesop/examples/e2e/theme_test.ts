import {test, expect} from '@playwright/test';

test('theme', async ({page}) => {
  await page.emulateMedia({colorScheme: 'dark'});
  await page.goto('/testing/theme');

  // Theme mode is auto & dark color scheme preferred -> dark theme
  await expect(page.getByText('Theme: dark')).toBeVisible();
  expect(await page.evaluate(hasDarkTheme)).toBeTruthy();

  await page.getByRole('button', {name: 'toggle theme'}).click();

  // Theme mode is light -> light theme
  await expect(page.getByText('Theme: light')).toBeVisible();
  expect(await page.evaluate(hasDarkTheme)).toBeFalsy();

  await page.getByRole('button', {name: 'toggle theme'}).click();

  // Theme mode is dark -> dark theme
  await expect(page.getByText('Theme: dark')).toBeVisible();
  expect(await page.evaluate(hasDarkTheme)).toBeTruthy();
});

function hasDarkTheme() {
  return document.body.classList.contains('dark-theme');
}
