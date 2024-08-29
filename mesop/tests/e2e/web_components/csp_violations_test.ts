import {expect} from '@playwright/test';
import {testInProdOnly} from '../e2e_helpers';

// Prevent regression where JS modules were loaded on every page,
// and not just pages where it was needed.
testInProdOnly(
  'test CSP violations (from web components) are not shown on home page',
  async ({page}) => {
    const cspViolations: string[] = [];

    // Listen for CSP violations
    page.on('console', (msg) => {
      if (
        msg.type() === 'error' &&
        msg.text().includes('Content Security Policy')
      ) {
        cspViolations.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    expect(cspViolations).toHaveLength(0);
  },
);
