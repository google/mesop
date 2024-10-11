import {test, expect} from '@playwright/test';

test.describe('Sidenav component', () => {
  test('open/close sidenav', async ({page}) => {
    await page.goto('/components/sidenav/e2e/sidenav_app');
    await (await page.locator('button').filter({hasText: 'menu'})).click();
    await expect(await page.getByText('Inside sidenav')).toBeVisible();
    await (await page.locator('button').filter({hasText: 'menu'})).click();
    await expect(await page.getByText('Inside sidenav')).toBeHidden();
  });

  test('escape closes sidenav', async ({page}) => {
    await page.goto('/components/sidenav/e2e/sidenav_app');
    const mainContent = await page.getByText('Main content');
    const startLocation = await mainContent.boundingBox();
    await (await page.locator('button').filter({hasText: 'menu'})).click();
    await expect(await page.getByText('Inside sidenav')).toBeVisible();
    const midLocation = await mainContent.boundingBox();
    // Main content should be pushed over to the left when sidenav is opened.
    expect(startLocation!.x).toBeLessThan(midLocation!.x);
    await page.getByText('Inside sidenav').click();
    await page.keyboard.press('Escape');
    await expect(await page.getByText('Inside sidenav')).toBeHidden();
    // Make sure the main content has moved back to original position after sidenav
    // has closed. Fix for GH-1019.
    const endLocation = await mainContent.boundingBox();
    expect(startLocation!.x).toEqual(endLocation!.x);
  });

  test('escape does not close sidenav if disable_close=True', async ({
    page,
  }) => {
    await page.goto('/components/sidenav/e2e/sidenav_app_no_esc');
    await (await page.locator('button').filter({hasText: 'menu'})).click();
    await expect(await page.getByText('Inside sidenav')).toBeVisible();
    await page.getByText('Inside sidenav').click();
    await page.keyboard.press('Escape');
    await expect(await page.getByText('Inside sidenav')).toBeVisible();
  });

  test('show sidenav on the right side', async ({page}) => {
    await page.goto('/components/sidenav/e2e/sidenav_app_position');
    await (await page.locator('button').filter({hasText: 'menu'})).click();
    const sidenav = await page.getByText('Inside sidenav');
    await expect(sidenav).toBeVisible();
    const sidenavLocation = await sidenav.boundingBox();
    // During manually testing the x position of the sidenav with position start was
    // approx -130. With position end, the position was approx 1,200. So we'll just
    // check the x position is greater than 0 since browser window width may change
    // depending on the machine.
    expect(sidenavLocation!.x).toBeGreaterThan(0);
  });
});
