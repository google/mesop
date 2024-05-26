import {test, expect} from '@playwright/test';

test('test slider behavior', async ({page}) => {
  await page.goto('/components/slider/e2e/slider_app');

  // Make sure the initial slider value is set to 50.
  const slider = await page.getByRole('slider');
  expect(await slider.evaluate((el) => el.value)).toBe('50');

  // Emulate moving the slider.
  await slider.evaluate((el, value) => {
    el.value = value;
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
  }, '20');
  // Should update the slider value and the text.
  expect(await slider.evaluate((el) => el.value)).toBe('20');
  expect(await page.getByText('Value: 20').textContent()).toContain(
    'Value: 20',
  );

  // Update the slider value via the textbox.
  await page.getByLabel('Slider value').fill('75');
  // Need to wait for the input state to be saved first.
  await page.waitForTimeout(2000);
  // Should update the slider value and the text.
  expect(await slider.evaluate((el) => el.value)).toBe('75');
  expect(await page.getByText('Value: 75').textContent()).toContain(
    'Value: 75',
  );
});
