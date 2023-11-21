# Pages

## Simple, 1-page setup

If you want to create a simple Optic app, you can do the following:

```python
import optic as op

@op.page()
def foo():
    op.text("bar")
```

This is the same as the following example which more explicitly sets the route to `"/"`.

## Explicit 1-page setup

```python
import optic as op

@op.page(path="/")
def foo():
    op.text("bar")
```

## Multi-page setup

```python
import optic as op

@op.page(path="/1")
def page1():
    op.text("page 1")

@op.page(path="/2")
def page2():
    op.text("page 2")
```
