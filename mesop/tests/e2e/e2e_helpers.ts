import {test as base} from '@playwright/test';

export const testInProdOnly = base.extend({
  // Skip all tests in this file if MESOP_DEBUG_MODE is 'true'
  page: async ({page}, use) => {
    if (process.env.MESOP_DEBUG_MODE === 'true') {
      base.skip(true, 'Skipping test in debug mode');
    }
    await use(page);
  },
});
