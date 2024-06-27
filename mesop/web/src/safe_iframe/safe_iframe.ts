/**
 * This file approximates a downstream implementation. Be careful about
 * changing this file to avoid unintended deviations between open-source and downstream.
 */

import {sanitizeJavaScriptUrl} from './sanitize_javascript_url';

/**
 * setIframeSrc is a safe wrapper for setting an iframe src.
 */
export function setIframeSrc(iframe: HTMLIFrameElement, src: string) {
  // Intentionally delegate to an impl function because the following
  // line will be modified downstream.
  setIframeSrcImpl(iframe, src);
}

// copybara:strip_begin(external-only)
function setIframeSrcImpl(iframe: HTMLIFrameElement, src: string) {
  // This is a tightly controlled list of attributes that enables us to
  // secure sandbox iframes. Do not add additional attributes without
  // consulting a security resource.
  //
  // Ref:
  // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox
  iframe.sandbox.add(
    'allow-same-origin',
    'allow-scripts',
    'allow-forms',
    'allow-popups',
    'allow-popups-to-escape-sandbox',
    'allow-storage-access-by-user-activation',
  );

  iframe.src = sanitizeJavaScriptUrl(src)!;
}
// copybara:strip_end
