# Multi-Pages

You can define multi-page Mesop applications by using the page feature you learned from [Core Concepts](../getting-started/core-concepts.md).

## Multi-page setup

```python
import mesop as me

@me.page(path="/1")
def page1():
    me.text("page 1")

@me.page(path="/2")
def page2():
    me.text("page 2")
```

Learn more about page configuration in the [page API doc](../api/page.md).

## Navigation

If you have multiple pages, you will typically want to navigate from one page to another when the user clicks a button. You can use `me.navigate("/to/path")` to navigate to another page.

**Example:**

```python
--8<-- "mesop/examples/docs/multi_page_nav.py"
```

> Note: you can re-use state across pages. See how the above example uses the `State#count` value across pages.
