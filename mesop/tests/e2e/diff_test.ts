import {test, expect} from '@playwright/test';

test('test component diffing', async ({page}) => {
  await page.goto('/testing/complex_layout');

  // Spot check initial page render.
  let locator = await page.locator('div:has-text("Label")');
  await expect(locator).toHaveCount(7);
  await expect(locator.first()).toHaveText('Label red');
  await expect(locator.nth(4)).toHaveText('Label blue');
  await expect(locator.last()).toHaveText('Label violet');
  await expect(page.locator('//input')).toHaveCount(0);

  // Test general diff updates updates
  await page.getByRole('button', {name: 'Reverse colors'}).click();
  locator = await page.locator('div:has-text("Label")');
  await expect(locator).toHaveCount(7);
  await expect(locator.first()).toHaveText('Label violet');
  await expect(locator.nth(4)).toHaveText('Label yellow');
  await expect(locator.last()).toHaveText('Label red');

  // Test diff propagation
  await page.getByRole('button', {name: 'Update last color'}).click();
  locator = await page.locator('div:has-text("Label")');
  await expect(locator).toHaveCount(7);
  await expect(locator.first()).toHaveText('Label violet');
  await expect(locator.nth(4)).toHaveText('Label yellow');
  await expect(locator.last()).toHaveText('Label white');

  // Test adding components to differents parts of tree
  await page.getByRole('button', {name: 'Show random inputs'}).click();
  locator = await page.locator(
    '//component-renderer[contains(@style, "border")]//input',
  );
  await expect(locator.first()).toHaveAttribute('type', 'checkbox');
  await expect(locator.nth(1)).toHaveAttribute('type', 'text');
  await expect(locator.nth(2)).toHaveAttribute('type', 'radio');
  await expect(locator.nth(3)).toHaveAttribute('type', 'radio');
  await expect(locator.last()).toHaveAttribute('type', 'range');
  locator = await page.locator(
    '//component-renderer[contains(@style, "white")]//input',
  );
  await expect(locator.first()).toHaveAttribute('type', 'text');
  await expect(locator.nth(1)).toHaveAttribute('type', 'checkbox');
  await expect(locator.nth(2)).toHaveAttribute('type', 'range');
  await expect(locator.nth(3)).toHaveAttribute('type', 'radio');
  await expect(locator.nth(4)).toHaveAttribute('type', 'radio');

  // Test replacement of components to differenet components
  await page.getByRole('button', {name: 'Show other random inputs'}).click();
  locator = await page.locator(
    '//component-renderer[contains(@style, "border")]//input',
  );
  await expect(locator.first()).toHaveAttribute('type', 'checkbox');
  await expect(locator.nth(1)).toHaveAttribute('type', 'radio');
  await expect(locator.nth(2)).toHaveAttribute('type', 'radio');
  await expect(locator.last()).toHaveAttribute('type', 'text');
  locator = await page.locator(
    '//component-renderer[contains(@style, "white")]//input',
  );
  await expect(locator.first()).toHaveAttribute('type', 'checkbox');
  await expect(locator.nth(1)).toHaveAttribute('type', 'text');
  await expect(locator.last()).toHaveAttribute('type', 'radio');

  // Test deletion of components
  await page.getByRole('button', {name: 'Hide random inputs'}).click();
  await expect(page.locator('//input')).toHaveCount(0);
});
