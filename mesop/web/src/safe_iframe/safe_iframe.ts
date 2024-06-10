/**
 * This file approximates a downstream implementation. Be careful about
 * changing this file to avoid unintended deviations between open-source and downstream.
 */

import {DomSanitizer} from '@angular/platform-browser';
import {sanitizeJavaScriptUrl} from './sanitize_javascript_url';

export function setIframeSrc(iframe: HTMLIFrameElement, src: string) {
  // Intentionally delegate to an impl function because the following
  // line will be modified downstream.
  setIframeSrcImpl(iframe, src);
}

export function setIframeSrcDoc(
  iframe: HTMLIFrameElement,
  srcDoc: string,
  sanitizer: DomSanitizer,
) {
  // Intentionally delegate to an impl function because the following
  // line will be modified downstream.
  setIframeSrcDocImpl(iframe, srcDoc, sanitizer);
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

function setIframeSrcDocImpl(
  iframe: HTMLIFrameElement,
  srcdoc: string,
  sanitizer: DomSanitizer,
) {
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

  // SafeHTML can be assigned to srcdoc, but TS compiler doesn't know this.
  iframe.srcdoc = sanitizer.bypassSecurityTrustHtml(srcdoc) as string;
}
// copybara:strip_end
