import {Page, test, expect} from '@playwright/test';

const expectTitleUpdate = async (page: Page, title: string) => {
  return await expect(async () => {
    expect(await page.title()).toEqual(title);
  }).toPass({timeout: 5000});
};

test.describe('Update page title', () => {
  test('title updates', async ({page}) => {
    await page.goto('/update_page_title/page1');

    await page.getByText('update title').click();
    await expectTitleUpdate(page, 'Update title page 1');

    // Title should stay the same even though state is updated.
    await page.getByText('title does not change if clicked').click();
    await expectTitleUpdate(page, 'Update title page 1');
  });

  test.describe('navigation with separate yields', () => {
    test('title change before navigate uses page title', async ({page}) => {
      await page.goto('/update_page_title/page1');

      await page
        .getByRole('button', {
          name: 'title change before navigate',
          exact: true,
        })
        .click();
      await expect(page).toHaveURL(
        'http://127.0.0.1:32123/update_page_title/page2',
      );
      await expectTitleUpdate(page, 'Mesop: /update_page_title/page2');
    });

    test('title change after navigate uses custom page title', async ({
      page,
    }) => {
      await page.goto('/update_page_title/page1');

      await page
        .getByRole('button', {name: 'title change after navigate', exact: true})
        .click();
      await expect(page).toHaveURL(
        'http://127.0.0.1:32123/update_page_title/page2',
      );
      await expectTitleUpdate(page, 'Update Page 2');
    });
  });

  test.describe('navigation with grouped yields', () => {
    test('title change before navigate uses page title', async ({page}) => {
      await page.goto('/update_page_title/page1');

      await page
        .getByRole('button', {
          name: '(grouped) title change before navigate',
          exact: true,
        })
        .click();
      await expect(page).toHaveURL(
        'http://127.0.0.1:32123/update_page_title/page2',
      );
      await expectTitleUpdate(page, 'Mesop: /update_page_title/page2');
    });

    test('title change after navigate uses custom page title', async ({
      page,
    }) => {
      await page.goto('/update_page_title/page1');

      await page
        .getByRole('button', {
          name: '(grouped) title change after navigate',
          exact: true,
        })
        .click();
      await expect(page).toHaveURL(
        'http://127.0.0.1:32123/update_page_title/page2',
      );
      await expectTitleUpdate(page, 'Update Page 2');
    });
  });

  test.describe('navigation with mulitiple yields', () => {
    test('title change before navigate uses page title', async ({page}) => {
      await page.goto('/update_page_title/page1');

      await page
        .getByRole('button', {
          name: '(multi) title change before navigate',
          exact: true,
        })
        .click();
      await expect(page).toHaveURL(
        'http://127.0.0.1:32123/update_page_title/page3',
      );
      await expectTitleUpdate(page, 'Mesop: /update_page_title/page3');
    });

    test('title change after navigate uses custom page title', async ({
      page,
    }) => {
      await page.goto('/update_page_title/page1');

      await page
        .getByRole('button', {
          name: '(multi) title change after navigate',
          exact: true,
        })
        .click();
      await expect(page).toHaveURL(
        'http://127.0.0.1:32123/update_page_title/page3',
      );
      await expectTitleUpdate(page, 'Update Page 3');
    });
  });
});
