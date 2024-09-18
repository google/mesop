import {testInConcurrentUpdatesEnabledOnly} from './e2e_helpers';
import {expect} from '@playwright/test';

testInConcurrentUpdatesEnabledOnly('concurrent updates', async ({page}) => {
  await page.goto('/concurrent_updates');
  await page.getByRole('button', {name: 'Slow state update'}).click();
  await page.getByRole('button', {name: 'Fast state update'}).click();
  await expect(page.getByText('Fast state: 1')).toBeVisible();
  await expect(page.getByText('Slow state: 1')).toBeVisible();

  // Slow state will update after the next render loop.
  await expect(page.getByText('Slow state: 2')).toBeVisible();
});
