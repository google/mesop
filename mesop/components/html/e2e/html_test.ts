import {test, expect} from '@playwright/test';
import {testInProdOnly} from '../../../tests/e2e/e2e_helpers';

test('test sanitized html', async ({page}) => {
  await page.goto('/components/html/e2e/html_app');
  // mesop is the HTML link so we're checking that it's rendered.
  expect(await page.getByText('Custom HTML').textContent()).toContain(
    'mesoplink',
  );
});

test('test sandboxed html', async ({page}) => {
  await page.goto('/components/html/e2e/html_app');
  const snapshotName = 'iframe_sandbox_attributes';
  expect(
    await page
      .frameLocator('iframe')
      .locator('#iframe')
      .getAttribute('sandbox'),
  ).toMatchSnapshot(snapshotName);
  await expect(
    page
      .frameLocator('iframe')
      .frameLocator('#iframe')
      .getByText('iamsandboxed-0'),
  ).toBeVisible();

  await page.getByRole('button', {name: 'Increment sandboxed HTML'}).click();
  await expect(
    page
      .frameLocator('iframe')
      .frameLocator('#iframe')
      .getByText('iamsandboxed-1'),
  ).toBeVisible();
  // Should be the same as before:
  expect(
    await page
      .frameLocator('iframe')
      .locator('#iframe')
      .getAttribute('sandbox'),
  ).toMatchSnapshot(snapshotName);
});

test('test sandboxed html - origin is null', async ({page}) => {
  await page.goto('/components/html/e2e/html_origin_app');
  await expect(
    page
      .frameLocator('iframe')
      .frameLocator('#iframe')
      .getByText('origin: null'),
  ).toBeVisible();
});

testInProdOnly('sandbox_iframe.html csp', async ({page}) => {
  const response = await page.goto('/sandbox_iframe.html');
  const csp = response?.headers()['content-security-policy']!;
  expect(csp).toMatchSnapshot('sandbox_iframe.html-csp.txt');
});
