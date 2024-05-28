import mesop as me


@me.page(path="/scroll_into_view")
def app():
  me.button("Scroll to middle line", on_click=scroll_to_middle)
  me.button("Scroll to bottom line", on_click=scroll_to_bottom)
  for _ in range(100):
    me.text("Filler line")
  me.text("middle_line", key="middle_line")
  for _ in range(100):
    me.text("Filler line")
  me.text("bottom_line", key="bottom_line")


def scroll_to_middle(e: me.ClickEvent):
  me.scroll_into_view(key="middle_line")


def scroll_to_bottom(e: me.ClickEvent):
  me.scroll_into_view(key="bottom_line")
