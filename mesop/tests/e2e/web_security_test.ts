// http://localhost:32123/plot
import {test, expect} from '@playwright/test';

const EXPECTED_CSP =
  "default-src 'self'; font-src fonts.gstatic.com; frame-ancestors 'self' https:; frame-src 'self' https:; img-src 'self' data: https:; media-src 'self' data: https:; style-src 'self' 'nonce-{{NONCE}}' fonts.googleapis.com; style-src-attr 'unsafe-inline'; script-src 'self' 'nonce-{{NONCE}}'; trusted-types angular; require-trusted-types-for 'script'";

test('ensure web security best practices are followed', async ({page}) => {
  const response = await page.goto('/');
  const csp = response?.headers()['content-security-policy'];
  expect(
    csp
      // nonce is randomly generated so we need to replace it with a stable string.
      ?.replace(/nonce-\w+/g, 'nonce-{{NONCE}}')
      // A bit of formatting to make it easier to read.
      .replace(/; /g, '\n'),
  ).toMatchSnapshot('csp.txt');
});
