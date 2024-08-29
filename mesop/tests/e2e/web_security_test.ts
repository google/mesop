// http://localhost:32123/plot
import {expect} from '@playwright/test';
import {testInProdOnly} from './e2e_helpers';

testInProdOnly('csp: default', async ({page}) => {
  const response = await page.goto('/');
  const csp = response?.headers()['content-security-policy']!;
  expect(cleanCsp(csp)).toMatchSnapshot('csp.txt');
});

testInProdOnly('csp: allowed parent iframe origins', async ({page}) => {
  const response = await page.goto('/allowed_iframe_parents');
  const csp = response?.headers()['content-security-policy']!;
  expect(cleanCsp(csp)).toMatchSnapshot('csp_allowed_iframe_parents.txt');
});

testInProdOnly('csp escaping', async ({page}) => {
  const response = await page.goto('/testing/csp_escaping');
  const csp = response?.headers()['content-security-policy']!;
  expect(cleanCsp(csp)).toMatchSnapshot('csp_escaping.txt');
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
