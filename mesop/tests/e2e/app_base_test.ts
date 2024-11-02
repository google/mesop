import {test, expect} from '@playwright/test';

test.describe('MESOP_APP_BASE_PATH', () => {
  if (process.env['MESOP_APP_BASE_PATH'] === undefined) {
    test.skip('Test skipped because MESOP_APP_BASE_PATH is not set.');
  }
  test('serves static file relative to MESOP_APP_BASE_PATH', async ({page}) => {
    const response = await page.goto('/static/test.txt');
    expect(response!.status()).toBe(200);
    const text = await response!.text();
    expect(text).toContain('test MESOP_APP_BASE_PATH works');
  });
});
