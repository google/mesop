import {test, expect} from '@playwright/test';

test('test click event', async ({page}) => {
  await page.goto('/components/box/e2e/box_events_app');

  await page.mouse.click(100, 100);

  await expect(page.getByText('Is Click: True')).toBeVisible();
  await expect(page.getByText('Is Right Click: False')).toBeVisible();
  await expect(page.getByText('Client X: 100.0')).toBeVisible();
  await expect(page.getByText('Client Y: 100.0')).toBeVisible();
  await expect(page.getByText('Page X: 100.0')).toBeVisible();
  await expect(page.getByText('Page Y: 100.0')).toBeVisible();
  await expect(page.getByText('Offset X: 80.0')).toBeVisible();
  await expect(page.getByText('Offset Y: 6.0')).toBeVisible();
});

test('test right click event', async ({page}) => {
  await page.goto('/components/box/e2e/box_events_app');

  await page.mouse.click(100, 100, {button: 'right'});

  await expect(page.getByText('Is Click: True')).toBeVisible();
  await expect(page.getByText('Is Right Click: True')).toBeVisible();
  await expect(page.getByText('Client X: 100.0')).toBeVisible();
  await expect(page.getByText('Client Y: 100.0')).toBeVisible();
  await expect(page.getByText('Page X: 100.0')).toBeVisible();
  await expect(page.getByText('Page Y: 100.0')).toBeVisible();
  await expect(page.getByText('Offset X: 80.0')).toBeVisible();
  await expect(page.getByText('Offset Y: 6.0')).toBeVisible();
});
