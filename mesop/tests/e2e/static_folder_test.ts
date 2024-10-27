import {test, expect} from '@playwright/test';

test.describe('Static Folders', () => {
  test.describe('MESOP_STATIC_FOLDER disabled', () => {
    if (process.env['MESOP_STATIC_FOLDER'] !== undefined) {
      test.skip('Test skipped because MESOP_STATIC_FOLDER is set.');
    }
    test('static folder not viewable if MESOP_STATIC_FOLDER not enabled', async ({
      page,
    }) => {
      const response = await page.goto('/static/tailwind.css');
      expect(response!.status()).toBe(500);
    });
    test('default favicon is used', async ({page}) => {
      await page.goto('/tailwind');
      const faviconLink = await page
        .locator('link[rel="shortcut icon"]')
        .first();
      await expect(faviconLink).toHaveAttribute('href', './favicon.ico');
    });
  });

  test.describe('MESOP_STATIC_FOLDER enabled', () => {
    if (process.env['MESOP_STATIC_FOLDER'] === undefined) {
      test.skip('Test skipped because MESOP_STATIC_FOLDER is not set.');
    }

    test('static file viewable if exists', async ({page}) => {
      const response = await page.goto('/static/tailwind.css');
      expect(response!.status()).toBe(200);
    });
    test('static file not viewable if not exists', async ({page}) => {
      const response = await page.goto('/static/non-existent.css');
      expect(response!.status()).toBe(404);
    });
    test('moving down from the root path is not allowed', async ({page}) => {
      const response = await page.goto('/static/../config.py');
      expect(response!.status()).toBe(500);
    });
    test('custom favicon is used', async ({page}) => {
      await page.goto('/tailwind');
      const faviconLink = await page
        .locator('link[rel="shortcut icon"]')
        .first();
      await expect(faviconLink).toHaveAttribute('href', '/static/favicon.ico');
    });
  });
});
