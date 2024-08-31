import {test, expect} from '@playwright/test';

test('scroll_into_view', async ({page}) => {
  await page.goto('/scroll_into_view');
  await page.setViewportSize({width: 200, height: 200});

  await expect(page.getByText('bottom_line')).not.toBeInViewport();

  await page
    .getByRole('button', {name: 'Scroll to bottom line', exact: true})
    .click();

  await expect(page.getByText('bottom_line')).toBeInViewport();
});

test('scroll_into_view - works with components rendered in same tick', async ({
  page,
}) => {
  await page.setViewportSize({width: 200, height: 200});
  await page.goto('/scroll_into_view_deferred');
  await expect(page.getByText('bottom line')).toBeInViewport();
});
