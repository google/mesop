# Layouts

Mesop takes an unopinionated approach to layout. It does not impose a specific layout on your app so you can build custom layouts. The crux of doing layouts in Mesop is the [Box component](../components/box.md) and using the [Style API](../api/style.md) which are Pythonic wrappers around the CSS layout model.

For most Mesop apps, you will use some combination of these types of layouts:

- [Rows and Columns](#rows-and-columns)
- [Grids](#grids)

## Common layout examples

To interact with the examples below, open the Mesop Layouts Colab: [![Open In Colab](../assets/colab.svg)](https://colab.research.google.com/github/google/mesop/blob/main/notebooks/mesop_layout_colab.ipynb)

### Rows and Columns

#### Basic Row

```python title="Basic Row"
def row():
    with me.box(style=me.Style(display="flex", flex_direction="row")):
        me.text("Left")
        me.text("Right")
```

#### Row with Spacing

```python title="Row with Spacing"
def row():
    with me.box(style=me.Style(display="flex", flex_direction="row", justify_content="space-around")):
        me.text("Left")
        me.text("Right")
```

#### Row with Alignment

```python title="Row with Alignment"
def row():
    with me.box(style=me.Style(display="flex", flex_direction="row", align_items="center")):
        me.box(style=me.Style(background="red", height=50, width="50%"))
        me.box(style=me.Style(background="blue", height=100, width="50%"))
```

#### Rows and Columns

```python title="Rows and Columns"
def app():
    with me.box(style=me.Style(display="flex", flex_direction="row", gap=16, height="100%")):
        column(1)
        column(2)
        column(3)

def column(num: int):
    with me.box(style=me.Style(
        flex_grow=1,
        background="#e0e0e0",
        padding=me.Padding.all(16),
        display="flex",
        flex_direction="column",
    )):
        me.box(style=me.Style(background="red", height=100))
        me.box(style=me.Style(background="blue", flex_grow=1))
```

### Grids

#### Side-by-side Grid

```python title="Side-by-side Grid"
def grid():
    # 1fr means 1 fraction, so each side is the same size.
    # Try changing one of the 1fr to 2fr and see what it looks like
    with me.box(style=me.Style(display="grid", grid_template_columns="1fr 1fr")):
        me.text("A bunch of text")
        me.text("Some more text")
```

#### Header Body Footer Grid

```python title="Header Body Footer Grid"
def app():
    with me.box(style=me.Style(
        display="grid",
        grid_template_rows="auto 1fr auto",
        height="100%"
    )):
        # Header
        with me.box(style=me.Style(
            background="#f0f0f0",
            padding=me.Padding.all(24)
        )):
            me.text("Header")

        # Body
        with me.box(style=me.Style(
            padding=me.Padding.all(24),
            overflow_y="auto"
        )):
            me.text("Body Content")
            # Add more body content here

        # Footer
        with me.box(style=me.Style(
            background="#f0f0f0",
            padding=me.Padding.all(24)
        )):
            me.text("Footer")
```

#### Sidebar Layout

```python title="Sidebar Layout"
def app():
    with me.box(style=me.Style(
        display="grid",
        grid_template_columns="250px 1fr",
        height="100%"
    )):
        # Sidebar
        with me.box(style=me.Style(
            background="#f0f0f0",
            padding=me.Padding.all(24),
            overflow_y="auto"
        )):
            me.text("Sidebar")

        # Main content
        with me.box(style=me.Style(
            padding=me.Padding.all(24),
            overflow_y="auto"
        )):
            me.text("Main Content")
```

#### Responsive UI

This is similar to the Grid Sidebar layout above, except on smaller screens, we will hide the sidebar. Try resizing the browser window and see how the UI changes.

Learn more about responsive UI in the [viewport size docs](../api/viewport-size.md).

```python
def app():
    is_desktop = me.viewport_size().width > 640
    with me.box(style=me.Style(
        display="grid",
        grid_template_columns="250px 1fr" if is_desktop else "1fr",
        height="100%"
    )):
        if is_desktop:
          # Sidebar
          with me.box(style=me.Style(
              background="#f0f0f0",
              padding=me.Padding.all(24),
              overflow_y="auto"
          )):
              me.text("Sidebar")

        # Main content
        with me.box(style=me.Style(
            padding=me.Padding.all(24),
            overflow_y="auto"
        )):
            me.text("Main Content")
```

## Learn more

For a real-world example of using these types of layouts, check out the Mesop Showcase app:

- [App](https://google.github.io/mesop/showcase/)
- [Code](https://github.com/google/mesop/blob/main/showcase/main.py)

To learn more about flexbox layouts (rows and columns), check out:

- [CSS Tricks Guide to Flexbox Layouts](https://css-tricks.com/snippets/css/a-guide-to-flexbox/#aa-flexbox-properties)
- [MDN Flexbox guide](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox)

To learn more about grid layouts, check out:

- [CSS Tricks Guide to Grid Layouts](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [MDN Grid guide](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Grids)
