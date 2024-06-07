# Pages

You can define multi-page Mesop applications by using the page feature you learned from [Getting Started](../getting_started.md)

## Simple, 1-page setup

To create a simple Mesop app, you can use `me.page()` like this:

```python
import mesop as me

@me.page()
def foo():
    me.text("bar")
```

> NOTE: If you do not provide a `path` argument, then it defaults to the root path `"/"`.

## Explicit 1-page setup

This is the same as the above example which explicitly sets the route to `"/"`.

```python
import mesop as me

@me.page(path="/")
def foo():
    me.text("bar")
```

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

## Navigation

If you have multiple pages, you will typically want to navigate from one page to another when the user clicks a button. You can use `me.navigate("/to/path")` to navigate to another page.

**Example:**

```python
--8<-- "mesop/examples/docs/multi_page_nav.py"
```

> Note: you can re-use state across pages. See how the above example uses the `State#count` value across pages.

## `on_load`

You may want to do some sort of data-processing when a page is first loaded in a session.

### Examples

#### Simple handler

An `on_load` handler is similar to a regular event handler where you can mutate state.

```python
--8<-- "mesop/examples/docs/on_load.py"
```

#### Generator handler

The `on_load` handler can also be a generator function. This is useful if you need to call a slow or streaming API and want to return intermediate results before all the data has been received.

```python
--8<-- "mesop/examples/docs/on_load_generator.py"
```

## API

::: mesop.features.page.page

::: mesop.events.events.LoadEvent
