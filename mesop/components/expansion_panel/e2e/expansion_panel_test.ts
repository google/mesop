import {test, expect} from '@playwright/test';

test.describe('Expansion Panel', () => {
  test('basic render', async ({page}) => {
    await page.goto('/components/expansion_panel/e2e/expansion_panel_app');
    await expect(await page.getByText('Grapefruit content.')).toBeHidden();
    await page.getByText('Grapefruit title').click();
    await expect(await page.getByText('Grapefruit content.')).toBeVisible();
    await page.getByText('Grapefruit title').click();
    await expect(await page.getByText('Grapefruit content.')).toBeHidden();
  });

  test('disabled panel', async ({page}) => {
    await page.goto('/components/expansion_panel/e2e/expansion_panel_app');
    await expect(
      await page.locator('[aria-disabled="true"]').textContent(),
    ).toContain('Pineapple title');
  });

  test('hidden toggle', async ({page}) => {
    await page.goto('/components/expansion_panel/e2e/expansion_panel_app');
    await expect(
      await page
        .locator('[aria-disabled="false"] span.mat-content-hide-toggle')
        .textContent(),
    ).toContain('Cantalope title');
  });
});

test.describe('Accordion (single expanded panel)', () => {
  test('hidden toggle', async ({page}) => {
    await page.goto('/components/expansion_panel/e2e/accordion_app');
    await expect(await page.getByText('Pie content.')).toBeVisible();
    await expect(await page.getByText('Donut content.')).toBeHidden();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Donut title').click();
    await expect(await page.getByText('Pie content.')).toBeHidden();
    await expect(await page.getByText('Donut content.')).toBeVisible();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Donut title').click();
    await expect(await page.getByText('Pie content.')).toBeHidden();
    await expect(await page.getByText('Donut content.')).toBeHidden();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Ice cream title').click();
    await expect(await page.getByText('Pie content.')).toBeHidden();
    await expect(await page.getByText('Donut content.')).toBeHidden();
    await expect(await page.getByText('Ice cream content.')).toBeVisible();
  });
});

test.describe('Accordion (multiple expanded panels)', () => {
  test('multiple expansions allowed', async ({page}) => {
    await page.goto('/components/expansion_panel/e2e/multi_accordion_app');
    await expect(await page.getByText('Pie content.')).toBeHidden();
    await expect(await page.getByText('Donut content.')).toBeHidden();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Open All').click();
    await expect(await page.getByText('Pie content.')).toBeVisible();
    await expect(await page.getByText('Donut content.')).toBeVisible();
    await expect(await page.getByText('Ice cream content.')).toBeVisible();

    await page.getByText('Close All').click();
    await expect(await page.getByText('Pie content.')).toBeHidden();
    await expect(await page.getByText('Donut content.')).toBeHidden();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Donut title').click();
    await expect(await page.getByText('Pie content.')).toBeHidden();
    await expect(await page.getByText('Donut content.')).toBeVisible();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Pie title').click();
    await expect(await page.getByText('Pie content.')).toBeVisible();
    await expect(await page.getByText('Donut content.')).toBeVisible();
    await expect(await page.getByText('Ice cream content.')).toBeHidden();

    await page.getByText('Ice cream title').click();
    await expect(await page.getByText('Pie content.')).toBeVisible();
    await expect(await page.getByText('Donut content.')).toBeVisible();
    await expect(await page.getByText('Ice cream content.')).toBeVisible();

    await page.getByText('Donut title').click();
    await expect(await page.getByText('Pie content.')).toBeVisible();
    await expect(await page.getByText('Donut content.')).toBeHidden();
    await expect(await page.getByText('Ice cream content.')).toBeVisible();
  });
});
