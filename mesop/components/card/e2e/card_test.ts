import {test, expect} from '@playwright/test';

test.describe('Card', () => {
  test('renders card', async ({page}) => {
    await page.goto('/components/card/e2e/card_app');
    expect(
      await page
        .locator('mat-card')
        .evaluate((el) => el.classList.contains('mat-mdc-card-outlined')),
    ).toBeTruthy();
    expect(await page.locator('mat-card-title').textContent()).toContain(
      'Grapefruit',
    );
    expect(await page.locator('mat-card-subtitle').textContent()).toContain(
      'Kind of fruit',
    );
    expect(await page.locator('mat-card-content').textContent()).toContain(
      'Lorem ipsum dolor sit amet',
    );
    expect(
      await page
        .locator('mat-card-actions')
        .evaluate((el) =>
          el.classList.contains('mat-mdc-card-actions-align-end'),
        ),
    ).toBeTruthy();
    expect(await page.getByRole('button')).toHaveCount(2);
  });
});
