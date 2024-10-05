import {test} from '@playwright/test';

test.describe('Button Toggle', () => {
  test('single selection', async ({page}) => {
    await page.goto('/components/button_toggle/e2e/single_button_toggle_app');
    await page.getByText('Select button: bold').isVisible();
    await page.getByLabel('Bold').click();
    await page.getByText('Select buttons: ').isVisible();
    await page.getByLabel('Italic').click();
    await page.getByText('Select button: italic').isVisible();
    await page.getByLabel('Underline').click();
    await page.getByText('Select button: underline').isVisible();
  });

  test('multiple selection', async ({page}) => {
    await page.goto('/components/button_toggle/e2e/multiple_button_toggle_app');
    await page.getByText('Select buttons: bold underline').isVisible();
    await page.getByLabel('Bold').click();
    await page.getByText('Select buttons: underline').isVisible();
    await page.getByLabel('Italic').click();
    await page.getByText('Select buttons: italic underline').isVisible();
  });

  test('disabled', async ({page}) => {
    await page.goto('/components/button_toggle/e2e/disabled_button_toggle_app');
    await page.getByText('Select button: bold').isVisible();
    await page.getByLabel('Bold').click();
    await page.getByText('Select button: bold').isVisible();
    await page.getByLabel('Italic').click();
    await page.getByText('Select buttons: bold').isVisible();
  });
});
