// http://localhost:32123/plot
import {test, expect} from '@playwright/test';

test('csp: default', async ({page}) => {
  const response = await page.goto('/');
  const csp = response?.headers()['content-security-policy']!;
  expect(cleanCsp(csp)).toMatchSnapshot('csp.txt');
});

test('csp: allowed parent iframe origins', async ({page}) => {
  const response = await page.goto('/allowed_iframe_parents');
  const csp = response?.headers()['content-security-policy']!;
  expect(cleanCsp(csp)).toMatchSnapshot('csp_allowed_iframe_parents.txt');
});

function cleanCsp(csp: string): string {
  return (
    csp
      // nonce is randomly generated so we need to replace it with a stable string.
      .replace(/'nonce-(.*?)'/g, "'nonce-{{NONCE}}'")
      // A bit of formatting to make it easier to read.
      .replace(/; /g, '\n')
  );
}
