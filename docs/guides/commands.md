# Commands

Commands are actions that you typically call within an event handler.

## Navigate

To navigate to another page, you can use `me.navigate`. This is particularly useful for navigating across a [multi-page](./pages.md) app.

### Example

```py

me.navigate('/path/to/navigate')

```

### API

::: mesop.commands.navigate.navigate

## Scroll into view

If you want to scroll a component into the viewport, you can use `me.scroll_into_view` which scrolls the component with the specified key into the viewport.

### Example

```python
--8<-- "mesop/examples/scroll_into_view.py"
```

### API

::: mesop.commands.scroll_into_view.scroll_into_view
