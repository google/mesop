import {test, expect} from '@playwright/test';
import path from 'path';

test('test upload file', async ({page}) => {
  await page.goto('/components/uploader/e2e/uploader_app');
  const fileChooserPromise = page.waitForEvent('filechooser');

  await page.getByText('Upload Image').click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(path.join(__dirname, 'mesop_robot.jpeg'));

  await expect(page.getByText('File name: mesop_robot.jpeg')).toHaveCount(1);
  await expect(page.getByText('File size: 30793')).toHaveCount(1);
  await expect(page.getByText('File type: image/jpeg')).toHaveCount(1);
  await expect(
    page.locator(`//img[contains(@src, "data:image/jpeg;base64")]`),
  ).toHaveCount(1);
});
