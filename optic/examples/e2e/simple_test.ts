import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("/");
  expect(await page.getByText("0 clicks").textContent()).toContain("0 clicks");

  await page.getByRole("button", { name: "click me" }).click();

  expect(await page.getByText("1 clicks").textContent()).toContain("1 clicks");
});
