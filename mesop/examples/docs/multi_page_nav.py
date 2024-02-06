import mesop as me


def on_click(e: me.ClickEvent):
  state = me.state(State)
  state.count += 1
  me.navigate("/multi_page_nav/page_2")


@me.page(path="/multi_page_nav")
def main_page():
  me.button("Navigate to Page 2", on_click=on_click)


@me.page(path="/multi_page_nav/page_2")
def page_2():
  state = me.state(State)
  me.text(f"Page 2 - count: {state.count}")


@me.stateclass
class State:
  count: int
