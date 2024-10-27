import {test, expect} from '@playwright/test';

test('web components - update children has no error', async ({page}) => {
  await page.goto('/web_component/dynamic_slot/dynamic_slot_app');

  const consoleErrors: string[] = [];

  // Listen for console errors
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  // Toggling the checkbox causes web component children to be updated.
  await page.getByRole('checkbox').check();
  await page.getByRole('checkbox').check();
  await page.getByRole('checkbox').check();

  // Specifically looking for errors like the following
  // which are signs that we're incorrectly updating the children:
  // NotFoundError: Failed to execute 'removeChild' on 'Node': The node to be removed is not a child of this node.
  expect(consoleErrors).toHaveLength(0);
});
