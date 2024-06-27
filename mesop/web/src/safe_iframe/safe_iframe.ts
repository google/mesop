/**
 * This file approximates a downstream implementation. Be careful about
 * changing this file to avoid unintended deviations between open-source and downstream.
 */

import {sanitizeJavaScriptUrl} from './sanitize_javascript_url';

/**
 * setIframeSrc is a safe wrapper for setting an iframe src.
 * Be explicit about the rationale on whether allowSameOrigin should be enabled
 * at the callsite, because there's major security implications.
 */
export function setIframeSrc(
  iframe: HTMLIFrameElement,
  src: string,
  options: {allowSameOrigin: boolean},
) {
  // Intentionally delegate to an impl function because the following
  // line will be modified downstream.
  setIframeSrcImpl(iframe, src, options);
}

// copybara:strip_begin(external-only)
function setIframeSrcImpl(
  iframe: HTMLIFrameElement,
  src: string,
  options: {allowSameOrigin: boolean},
) {
  // This is a tightly controlled list of attributes that enables us to
  // secure sandbox iframes. Do not add additional attributes without
  // consulting a security resource.
  //
  // Ref:
  // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox
  iframe.sandbox.add(
    'allow-scripts',
    'allow-forms',
    'allow-popups',
    'allow-popups-to-escape-sandbox',
    'allow-storage-access-by-user-activation',
  );
  if (options.allowSameOrigin) {
    iframe.sandbox.add('allow-same-origin');
  }

  iframe.src = sanitizeJavaScriptUrl(src)!;
}
// copybara:strip_end
