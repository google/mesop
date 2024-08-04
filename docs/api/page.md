# Page API

## Overview

Pages allow you to build multi-page applications by decorating Python functions with `me.page`. To learn more, read the see [multi-pages guide](../guides/multi-pages.md).

## Examples

### Simple, 1-page setup

To create a simple Mesop app, you can use `me.page()` like this:

```python
import mesop as me

@me.page()
def foo():
    me.text("bar")
```

> NOTE: If you do not provide a `path` argument, then it defaults to the root path `"/"`.

### Explicit 1-page setup

This is the same as the above example which explicitly sets the route to `"/"`.

```python
import mesop as me

@me.page(path="/")
def foo():
    me.text("bar")
```

## API

::: mesop.features.page.page
::: mesop.security.security_policy.SecurityPolicy
::: mesop.events.events.LoadEvent

## `on_load`

You may want to do some sort of data-processing when a page is first loaded in a session.

### Simple handler

An `on_load` handler is similar to a regular event handler where you can mutate state.

```python
--8<-- "mesop/examples/docs/on_load.py"
```

### Generator handler

The `on_load` handler can also be a generator function. This is useful if you need to call a slow or streaming API and want to return intermediate results before all the data has been received.

```python
--8<-- "mesop/examples/docs/on_load_generator.py"
```
