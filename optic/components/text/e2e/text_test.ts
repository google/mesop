import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("/components/text/e2e/text_app");
  expect(await page.getByText("Hello, world!").textContent()).toContain(
    "Hello, world!",
  );
});
