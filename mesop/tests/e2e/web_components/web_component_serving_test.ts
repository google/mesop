import {test, expect} from '@playwright/test';

test('web components serving blocks non-js/css files', async ({page}) => {
  const response = await page.goto(
    '/__web-components-module__/mesop/mesop/examples/web_component/quickstart/counter_component.py',
  );
  expect(response!.status()).toBe(500);
});

test('web components serving allows js and css files', async ({page}) => {
  const jsResponse = await page.goto(
    '/__web-components-module__/mesop/mesop/examples/web_component/quickstart/counter_component.js',
  );
  expect(jsResponse!.status()).toBe(200);

  const cssResponse = await page.goto(
    '/__web-components-module__/mesop/mesop/examples/web_component/testing.css',
  );
  expect(cssResponse!.status()).toBe(200);
});
