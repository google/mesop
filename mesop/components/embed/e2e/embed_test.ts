import {test, expect} from '@playwright/test';

test('test', async ({page}) => {
  await page.goto('/components/embed/e2e/embed_app');
  let iframe = await page.waitForSelector(
    'iframe[src="https://google.github.io/mesop/"]',
  );
  const snapshotName = 'iframe_sandbox_attributes';
  expect(await iframe.getAttribute('sandbox')).toMatchSnapshot(snapshotName);
  let frame = await iframe.contentFrame();
  await frame!.waitForLoadState('load');

  await page.click('button');

  // Check that iframe has reloaded to a new URL.
  iframe = await page.waitForSelector(
    'iframe[src="https://google.github.io/mesop/internal/publishing/"]',
  );
  frame = await iframe.contentFrame();
  await frame!.waitForLoadState('load');
  // Sandbox attributes should be the same:
  expect(await iframe.getAttribute('sandbox')).toMatchSnapshot(snapshotName);
});
