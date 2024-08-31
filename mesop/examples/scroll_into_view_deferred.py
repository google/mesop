import mesop as me


@me.stateclass
class State:
  show_bottom_line: bool = False


def on_load(e: me.LoadEvent):
  me.scroll_into_view(key="bottom_line")
  state = me.state(State)
  state.show_bottom_line = True


@me.page(path="/scroll_into_view_deferred", on_load=on_load)
def app():
  me.text("Scroll into view deferred")
  for _ in range(100):
    me.text("filler line")
  state = me.state(State)
  if state.show_bottom_line:
    me.text("bottom line", key="bottom_line")
