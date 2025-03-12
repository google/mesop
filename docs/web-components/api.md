# Web Components API

> Note: Web components were previously launched under the labs namespace (i.e. `import mesop.lab as mel`). As part of the v1 release, all of the web component APIs are now exposed in the main mesop namespace (i.e. `import mesop as me`). You can continue to use the labs namespace for the web components API until v2 (which will happen much later).

**Example usage:**

```python
import mesop as me

@me.web_component(...)
def a_web_component():
    me.insert_web_component(...)
```

## API

::: mesop.component_helpers.web_component.web_component

::: mesop.insert_web_component

::: mesop.WebEvent

::: mesop.slot
