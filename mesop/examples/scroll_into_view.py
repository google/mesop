import time

import mesop as me


@me.stateclass
class State:
  more_lines: int = 0


@me.page(path="/scroll_into_view")
def app():
  me.button("Scroll to middle line", on_click=scroll_to_middle)
  me.button("Scroll to bottom line", on_click=scroll_to_bottom)
  me.button(
    "Scroll to bottom line & generate lines",
    on_click=scroll_to_bottom_and_generate_lines,
  )
  for _ in range(100):
    me.text("Filler line")
  me.text("middle_line", key="middle_line")
  for _ in range(100):
    me.text("Filler line")
  me.text("bottom_line", key="bottom_line")
  for _ in range(me.state(State).more_lines):
    me.text("More lines")


def scroll_to_middle(e: me.ClickEvent):
  me.scroll_into_view(key="middle_line")


def scroll_to_bottom(e: me.ClickEvent):
  me.scroll_into_view(key="bottom_line")


def scroll_to_bottom_and_generate_lines(e: me.ClickEvent):
  state = me.state(State)
  me.scroll_into_view(key="bottom_line")
  yield
  state.more_lines += 5
  time.sleep(1)
  yield
  state.more_lines += 5
  time.sleep(1)
  yield
  state.more_lines += 5
  time.sleep(1)
  yield
  state.more_lines += 5
  time.sleep(1)
  yield
