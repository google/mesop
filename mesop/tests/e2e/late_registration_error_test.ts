import {expect} from '@playwright/test';
import {testInProdOnly} from './e2e_helpers';

testInProdOnly(
  'register page too late should cause an error',
  async ({page}) => {
    await page.goto('/testing/error_register_page_too_late');

    await expect(
      page.getByText(
        'Sorry, there was an error. Please contact the developer.',
      ),
    ).toBeVisible();

    await page.goto('/testing/error_register_page_too_late/too_late_page');

    await expect(
      page.getByText(
        'User Error: Accessed path: /testing/error_register_page_too_late/too_late_page not registered',
      ),
    ).toBeVisible();
  },
);

testInProdOnly(
  'register web component too late should cause an error',
  async ({page}) => {
    await page.goto('/testing/error_register_web_component_too_late');

    await expect(
      page.getByText(
        'Sorry, there was an error. Please contact the developer.',
      ),
    ).toBeVisible();
  },
);
