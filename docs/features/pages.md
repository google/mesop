# Pages

## Simple, 1-page setup

If you want to create a simple Mesop app, you can do the following:

```python
import mesop as me

@me.page()
def foo():
    me.text("bar")
```

This is the same as the following example which more explicitly sets the route to `"/"`.

## Explicit 1-page setup

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
