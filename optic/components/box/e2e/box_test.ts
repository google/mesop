import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("/components/box/e2e/box_app");
  expect(await page.getByText("Hello, world!").textContent()).toContain(
    "Hello, world!",
  );
});
