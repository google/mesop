import {Page, expect} from '@playwright/test';

export async function diffHtml(page: Page, filename = 'after') {
  expect(
    prettyPrintHtml(
      await page.evaluate(() =>
        // Remove angular framework DOM markups, particularly those that include machine-generated ids which
        // are brittle.
        document.body.innerHTML
          .replace(
            /<span _ngcontent-ng-[0-9a-z]+="" style="display: none;"><\/span>/g,
            '',
          )
          .replace(/ _ngcontent-ng-[0-9a-z]+=""/g, '')
          .replace(/ _nghost-ng-[0-9a-z]+=""/g, '')
          .replace(/ ng-reflect-[\-a-z]+=".*?"/g, '')
          .replace(/<!--.*?-->/gs, ''),
      ),
    ),
  ).toMatchSnapshot(`${filename}.html`);
}

function prettyPrintHtml(htmlString: string): string {
  const tab = '  '; // Two space indentation.
  let formatted = '';
  let indent = ''; // The current indentation

  htmlString.split(/>\s*</).forEach((element) => {
    // If the element is a closing tag, decrease indentation
    if (element.match(/^\/\w/)) {
      indent = indent.substring(tab.length);
    }

    formatted += `${indent}<${element}>\n`;

    // If the element is an opening tag, increase indentation
    if (element.match(/^<?\w[^>]*[^\/]$/)) {
      indent += tab;
    }
  });

  // Clean-up extra "<" prefix and ">\n" postfix:
  return `${formatted.substring(1, formatted.length - 2).trim()}\n`;
}
