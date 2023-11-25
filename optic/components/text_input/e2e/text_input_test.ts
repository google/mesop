import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("/components/text_input/e2e/text_input_app");
  const textOutput = await page.getByText("Text output:");
  expect(textOutput).toHaveText("Text output:initial_text_state");

  // await page.getByLabel("simple-text-input").click();
  await page.getByLabel("simple-text-input").fill("abcdef");
  await page.locator("html").click();
  // const textInput = await page.getByText("simple-text-input");
  // await textInput.fill("entered_text");
  // await textInput.blur();

  // const progressBar = await page.getByTestId("connection-progress-bar");
  // await progressBar.waitFor({ state: "hidden" });
  // await new Promise((s) => setTimeout(s, 1000));
  expect(textOutput).toHaveText("Text output:abcdef");
});
