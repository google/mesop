import mesop as me


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(path="/testing/theme", on_load=on_load)
def page():
  me.text("Theme: " + me.theme_brightness())
  me.button("toggle theme", on_click=toggle_theme)


def toggle_theme(e: me.ClickEvent):
  if me.theme_brightness() == "dark":
    me.set_theme_mode("light")
  else:
    me.set_theme_mode("dark")
