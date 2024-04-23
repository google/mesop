////////////////////////////////////////////////
// The following implementation was forked from:
// https://github.com/google/safevalues/blob/b17e6b77299afdf6af05bd13841793b34314b012/src/builders/url_builders.ts#L66
////////////////////////////////////////////////

/**
 * Checks that the URL scheme is not javascript.
 * The URL parsing relies on the URL API in browsers that support it.
 * @param url The URL to sanitize for a SafeUrl sink.
 * @return undefined if url has a javascript: scheme, the original URL
 *     otherwise.
 */
export function sanitizeJavaScriptUrl(url: string): string | undefined {
  if (reportJavaScriptUrl(url)) {
    return undefined;
  }
  return url;
}

/**
 * A pattern that blocks javascript: URLs. Matches
 * (a) Urls with an explicit scheme that is not javascript and that only has
 *     alphanumeric or [.-+_] characters; or
 * (b) Urls with no explicit scheme. The pattern allows the first colon
 *     (`:`) character to appear after one of  the `/` `?` or `#` characters,
 *     which means the colon appears in path, query or fragment part of the URL.
 */
const IS_NOT_JAVASCRIPT_URL_PATTERN =
  /^\s*(?!javascript:)(?:[\w+.-]+:|[^:/?#]*(?:[/?#]|$))/i;

/**
 * Checks whether a urls has a `javascript:` scheme.
 * If the url has a `javascript:` scheme, reports it and returns true.
 * Otherwise, returns false.
 */
function reportJavaScriptUrl(url: string): boolean {
  const hasJavascriptUrlScheme = !IS_NOT_JAVASCRIPT_URL_PATTERN.test(url);
  if (hasJavascriptUrlScheme) {
    console.error(`A URL with content '${url}' was sanitized away.`);
  }
  return hasJavascriptUrlScheme;
}
