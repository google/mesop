import {test, expect} from '@playwright/test';

test('web components - make sure custom font does not cause CSP issues', async ({
  page,
}) => {
  await page.goto('/web_component/custom_font_csp_repro/custom_font_app');
  // Make sure page has loaded.
  expect(await page.getByText('Custom font: ').textContent()).toEqual(
    'Custom font: Inter Tight',
  );

  // Make sure the custom font is actually loaded.
  const isFontLoaded = await page.evaluate((fontName) => {
    return new Promise((resolve) => {
      if (document.fonts.check(`12px "${fontName}"`)) {
        resolve(true);
      } else {
        document.fonts.ready.then(() => {
          resolve(document.fonts.check(`12px "${fontName}"`));
        });
      }
    });
  }, 'Inter Tight');
  expect(isFontLoaded).toEqual(true);

  expect(await page.getByText('Value: ').textContent()).toEqual('Value: 10');
  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByText('Value: 9').textContent();
  await page.getByRole('button', {name: 'Decrement'}).click();
  await page.getByText('Value: 8').textContent();
});
