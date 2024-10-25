import {test as base} from '@playwright/test';

export const testInProdOnly = base.extend({
  // Skip this test if MESOP_DEBUG_MODE is 'true'
  page: async ({page}, use) => {
    if (process.env.MESOP_DEBUG_MODE === 'true') {
      base.skip(true, 'Skipping test in debug mode');
    }
    await use(page);
  },
});

export const testInConcurrentUpdatesEnabledOnly = base.extend({
  // Skip this test if MESOP_CONCURRENT_UPDATES_ENABLED is not 'true'
  page: async ({page}, use) => {
    if (process.env.MESOP_CONCURRENT_UPDATES_ENABLED !== 'true') {
      base.skip(true, 'Skipping test in concurrent updates disabled mode');
    }
    await use(page);
  },
});

export const testInWebSocketsEnabledOnly = base.extend({
  // Skip this test if MESOP_WEBSOCKETS_ENABLED is not 'true'
  page: async ({page}, use) => {
    if (process.env.MESOP_WEBSOCKETS_ENABLED !== 'true') {
      base.skip(true, 'Skipping test in websockets disabled mode');
    }
    await use(page);
  },
});
