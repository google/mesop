// http://localhost:32123/plot
import {test, expect} from '@playwright/test';

test('ensure web security best practices are followed', async ({page}) => {
  const response = await page.goto('/');
  const csp = response?.headers()['content-security-policy'];
  expect(
    csp
      // nonce is randomly generated so we need to replace it with a stable string.
      ?.replace(/'nonce-(.*?)'/g, "'nonce-{{NONCE}}'")
      // A bit of formatting to make it easier to read.
      .replace(/; /g, '\n'),
  ).toMatchSnapshot('csp.txt');
});
