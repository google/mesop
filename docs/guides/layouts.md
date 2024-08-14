# Layouts

Mesop takes an unopinionated approach to layout. It does not impose a specific layout on your app. Instead, it provides a set of tools to help you build your app's layout.

## Basics

The crux of doing layouts in Mesop is the [Box component](../components/box.md) and using the [Style API](../api/style.md) which are Pythonic wrappers around the CSS layout model.

### Rows and columns

```python title="Row"
import mesop as me

@me.page()
def row():
    with me.box(style=me.Style(display="flex", flex_direction="row")):
        me.text("Left")
        me.text("Right")
```

### Grids

...

## Examples

...
