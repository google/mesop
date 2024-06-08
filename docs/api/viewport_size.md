# Viewport size

## Overview
The viewport size API allows you to access the current viewport size. This can be useful for creating responsive and adaptive designs that are suitable for the user's screen size.

## Examples

### Responsive Design

Responsive design is having a single fluid layout that adapts to all screen sizes.

You can use the viewport size to dynamically set the property of a style. This can be useful if you want to fit two boxes in a row for larger screens (e.g. desktop) and a single box for smaller screens (e.g. mobile) as shown in the example below:

```py
import mesop as me

@me.page()
def page():
    if me.viewport_size().width > 640:
        width = me.viewport_size().width / 2
    else:
        width = me.viewport_size().width
    for i in range(8):
      me.box(style=me.Style(width=width))
```

> Tip: Responsive design tends to take less work and is usually a good starting point.

### Adaptive Design

Adaptive design is having multiple fixed layouts for specific device categories at specific breakpoints, typically viewport width.

For example, oftentimes you will hide the nav component on a mobile device and instead show a hamburger menu, while for a larger device you will always show the nav component on the left side.

```py
import mesop as me

@me.page()
def page():
    if me.viewport_size().width > 480:
        nav_component()
        body()
    else:
        body(show_menu_button=True)
```

> Tip: Adaptive design tends to take more work and is best for optimizing complex mobile and desktop experiences.

## API

::: mesop.features.viewport_size.viewport_size

::: mesop.features.viewport_size.Size
