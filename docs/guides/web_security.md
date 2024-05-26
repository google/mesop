# Web Security

Mesop by default configures its apps to follow a set of web security best practices.

## How

At a high-level, Mesop is built on top of Angular which provides [built-in security protections](https://angular.io/guide/security) and Mesop configures a strict [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP).

Specifics:

- Mesop APIs do not allow arbitrary JavaScript execution in the main execution context. For example, the [markdown](../components/markdown.md) component sanitizes the markdown content and removes active HTML content like JavaScript.
- Mesop's default Content Security Policy prevents arbitrary JavaScript code from executing on the page unless it passes [Angular's Trusted Types](https://angular.io/guide/security#enforcing-trusted-types) polices.

## Iframe Security

To prevent [clickjacking](https://owasp.org/www-community/attacks/Clickjacking), Mesop apps, when running in prod mode (the default mode used when [deployed](../guides/deployment.md)), do not allow sites from any other origins to iframe the Mesop app.

> Note: pages from the same origin as the Mesop app can always iframe the Mesop app.

If you want to allow a trusted site to iframe your Mesop app, you can explicitly allow list the [sources](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors#sources) which can iframe your app by configuring the security policy for a particular page.

### Example

```py
import mesop as me


@me.page(
  path="/allows_iframed",
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.com"],
  ),
)
def app():
  me.text("Test CSP")
```

You can also use wildcards to allow-list multiple subdomains from the same site, such as: `https://*.example.com`.
