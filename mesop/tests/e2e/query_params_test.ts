import {test, expect} from '@playwright/test';

test('query_param: on_load hook', async ({page}) => {
  await page.goto('/examples/query_params');
  expect(await page.getByText('query_params={').textContent()).toEqual(
    `query_params={'on_load': ['loaded']}`,
  );
  await expect(page).toHaveURL(/\?on_load=loaded$/);
});

test('query_param: load with query param in URL', async ({page}) => {
  await page.goto('/examples/query_params?a=1');
  expect(await page.getByText('query_params={').textContent()).toEqual(
    `query_params={'a': ['1'], 'on_load': ['loaded']}`,
  );
  await expect(page).toHaveURL(/\?a=1&on_load=loaded$/);
});

test('query_param: URL encoding', async ({page}) => {
  await page.goto('/examples/query_params');
  await page
    .getByRole('button', {name: 'URL-encoded query param', exact: true})
    .click();
  await expect(
    page.getByText(
      `{'on_load': ['loaded'], 'url_encoded': ['&should-be-escaped=true']}`,
    ),
  ).toBeVisible();
  await expect(page).toHaveURL(
    /\?on_load=loaded&url_encoded=%26should-be-escaped%3Dtrue$/,
  );
});

test('query_param: navigate w/ URL encoding', async ({page}) => {
  await page.goto('/examples/query_params');
  await page
    .getByRole('button', {
      name: 'navigate URL-encoded query param',
      exact: true,
    })
    .click();
  await expect(
    page.getByText(
      `query_params(page_2)={'url_encoded': ['&should-be-escaped=true'], 'url_encoded_values': ['value1&a=1', 'value2&a=2']}`,
    ),
  ).toBeVisible();
  await expect(page).toHaveURL(
    /\?url_encoded=%26should-be-escaped%3Dtrue&url_encoded_values=value1%26a%3D1&url_encoded_values=value2%26a%3D2$/,
  );
});

test('query_param: multiple query param values for same key ', async ({
  page,
}) => {
  await page.goto('/examples/query_params');

  // Add a value for "list" key
  await page.getByRole('button', {name: 'append query param list'}).click();
  await expect(
    page.getByText(`query_params={'on_load': ['loaded'], 'list': ['val1']}`),
  ).toBeVisible();
  await expect(page).toHaveURL(/\?on_load=loaded&list=val1$/);

  // Add another value for "list" key
  await page.getByRole('button', {name: 'append query param list'}).click();
  await expect(
    page.getByText(
      `query_params={'on_load': ['loaded'], 'list': ['val1', 'val2']}`,
    ),
  ).toBeVisible();
  await expect(page).toHaveURL(/\?on_load=loaded&list=val1&list=val2$/);

  // Delete "list" query param
  await page.getByRole('button', {name: 'delete list query param'}).click();
  await expect(
    page.getByText(`query_params={'on_load': ['loaded']`),
  ).toBeVisible();
  await expect(page).toHaveURL(/\?on_load=loaded$/);
});

test('query_param: increment query param ', async ({page}) => {
  await page.goto('/examples/query_params');

  await page
    .getByRole('button', {name: 'increment query param directly'})
    .click();
  await expect(
    page.getByText(`query_params={'on_load': ['loaded'], 'counter': ['1']}`),
  ).toBeVisible();
  await expect(page).toHaveURL(/\?on_load=loaded&counter=1/);

  await page
    .getByRole('button', {name: 'increment query param directly'})
    .click();
  await expect(
    page.getByText(`query_params={'on_load': ['loaded'], 'counter': ['2']}`),
  ).toBeVisible();
  await expect(page).toHaveURL(/\?on_load=loaded&counter=2/);

  await page
    .getByRole('button', {name: 'increment query param by navigate'})
    .click();
  await expect(
    page.getByText(`query_params={'on_load': ['loaded'], 'counter': ['3']}`),
  ).toBeVisible();
  await expect(page).toHaveURL(/\?on_load=loaded&counter=3/);
});

test('query_param: delete all query params ', async ({page}) => {
  await page.goto('/examples/query_params');
  await page.getByRole('button', {name: 'append query param list'}).click();
  await page
    .getByRole('button', {name: 'increment query param directly'})
    .click();

  await page.getByRole('button', {name: 'delete all query params'}).click();
  await expect(page.getByText('query_params={}')).toBeVisible();
  await expect(page).toHaveURL(/^[^?]+$/); // Matches any URL without query parameters
});

test('query_param: navigate to another page with query params', async ({
  page,
}) => {
  await page.goto('/examples/query_params');
  await page
    .getByRole('button', {name: 'navigate to page 2 with query params'})
    .click();

  await expect(
    page.getByText(`query_params(page_2)={'on_load': ['loaded']}`),
  ).toBeVisible();
  // This isn't flaky because the page has finished navigated since we're checking
  // the page text above.
  expect(new URL(page.url()).search).toEqual('?on_load=loaded');
});

test('query_param: navigate to another page with dict', async ({page}) => {
  await page.goto('/examples/query_params');
  await page
    .getByRole('button', {name: 'navigate to page 2 with dict'})
    .click();

  await expect(
    page.getByText(
      `query_params(page_2)={'page2': ['1', '2'], 'single': ['a']}`,
    ),
  ).toBeVisible();
  // This isn't flaky because the page has finished navigated since we're checking
  // the page text above.
  expect(new URL(page.url()).search).toEqual('?page2=1&page2=2&single=a');
});

test('query_param: navigate to another page without query params', async ({
  page,
}) => {
  await page.goto('/examples/query_params');
  await page
    .getByRole('button', {name: 'navigate to page 2 without query params'})
    .click();

  await expect(page.getByText('query_params(page_2)={}')).toBeVisible();
  // This isn't flaky because the page has finished navigated since we're checking
  // the page text above.
  expect(new URL(page.url()).search).toEqual('');
});
