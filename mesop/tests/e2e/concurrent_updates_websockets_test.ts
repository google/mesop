import {testInWebSocketsEnabledOnly} from './e2e_helpers';
import {expect} from '@playwright/test';

testInWebSocketsEnabledOnly(
  'concurrent updates (websockets)',
  async ({page}) => {
    await page.goto('/concurrent_updates_websockets');
    await page.getByRole('button', {name: 'Slow state update'}).click();
    await page.getByRole('button', {name: 'Fast state update'}).click();
    await expect(page.getByText('Fast state: true')).toBeVisible();
    expect(await page.locator('text="Box!"').count()).toBe(1);
    await expect(page.getByText('Slow state: false')).toBeVisible();
    await expect(page.getByText('Slow state: true')).toBeVisible();
    //  Make sure there isn't a second Box from the concurrent update.
    expect(await page.locator('text="Box!"').count()).toBe(1);
  },
);
