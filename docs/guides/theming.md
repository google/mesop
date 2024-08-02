# Theming

Mesop has early-stage support for theming so you can support light theme and dark theme in a Mesop application.

## Dark Theming

For an actual example of using Mesop's theming API to support light theme and dark theme, we will look at the labs [chat component](../components/chat.md) which itself is written all in Python built on top of lower-level Mesop components.

### Theme toggle button

Inside the chat component, we've defined an icon button to toggle the theme so users can switch between light and dark theme:

```py
def toggle_theme(e: me.ClickEvent):
    if me.theme_brightness() == "light":
      me.set_theme_mode("dark")
    else:
      me.set_theme_mode("light")

with me.content_button(
    type="icon",
    style=me.Style(position="absolute", right=0),
    on_click=toggle_theme,
):
    me.icon("light_mode" if me.theme_brightness() == "dark" else "dark_mode")
```

### Using theme colors

You could define custom style logic to explicitly set the color based on the theme:

```py
def container():
  me.box(
    style=me.Style(
      background="white" if me.theme_brightness() == "light" else "black"
    )
  )
```

But this would be pretty tedious, so you can use theme variables like this:


```py
def container():
  me.box(style=me.Style(background=me.theme_var("background")))
```

This will use the appropriate background color for light theme and dark theme.

### Default theme mode

Finally, we want to use the default theme mode to "system" which means we will use the user's preferences for whether they want dark theme or light theme. For many users, their operating systems will automatically switch to dark theme during night time.

> Note: Mesop currently defaults to light theme mode but will eventually default to system theme mode in the future.

On our demo page with the chat component, we have a page [on_load](../api/page.md#on_load) event handler defined like this:

```py
def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")
```

## Theme Density

You can set the visual density of the Material components. By default, Mesop uses the least visually dense setting, i.e.

```py
me.set_theme_density(0) # 0 is the least dense
```

You can configure the density as an integer from 0 (least dense) to -4 (most dense). For example, if you want a medium-dense UI, you can do the following:

```py
def on_load(e: me.LoadEvent):
  me.set_theme_density(-2) # -2 is more dense than the default


@me.page(on_load=on_load)
def page():
  ...
```

## API

::: mesop.features.theme.set_theme_density
::: mesop.features.theme.set_theme_mode
::: mesop.features.theme.theme_brightness
::: mesop.features.theme.theme_var
::: mesop.features.theme.ThemeVar
