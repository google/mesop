## Overview

The HTML component allows you to add custom HTML to your Mesop app.

There are two modes for rendering HTML components:

- `sanitized` (default), where the HTML is [sanitized by Angular](https://angular.dev/best-practices/security#sanitization-example) to remove potentially unsafe code like `<script>` and `<style>` for web security reasons.
- `sandboxed`, which allows rendering of `<script>` and `<style>` HTML content by using an iframe sandbox.

## Examples

<iframe class="component-demo" src="https://mesop-y677hytkra-uc.a.run.app/html"></iframe>

```python
--8<-- "demo/html_demo.py"
```

## API

::: mesop.components.html.html.html
