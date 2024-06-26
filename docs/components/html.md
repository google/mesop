## Overview

The HTML component allows you to add custom HTML to your Mesop app.

By default, HTML components are rendered with `mode="sanitized"` which means the HTML is [sanitized by Angular](https://angular.dev/best-practices/security#sanitization-example) for web security reasons so potentially unsafe code like `<script>` and `<style>` are removed.

If you want to render `<script>` and `<style>` HTML content, use `mode="sandboxed"` instead which will render the HTML in an iframe.

## Examples

<iframe class="component-demo" src="https://mesop-y677hytkra-uc.a.run.app/html"></iframe>

```python
--8<-- "demo/html_demo.py"
```

## API

::: mesop.components.html.html.html
