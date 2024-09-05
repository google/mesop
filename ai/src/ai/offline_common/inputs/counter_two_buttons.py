import mesop as me


@me.stateclass
class State:
  count: int


def increment(e: me.ClickEvent):
  state = me.state(State)
  state.count += 1


def decrement(e: me.ClickEvent):
  state = me.state(State)
  state.count -= 1


@me.page()
def page():
  state = me.state(State)

  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=16,
      padding=me.Padding.all(16),
    )
  ):
    me.text(f"Count: {state.count}", type="headline-4")
    me.button("Increment", on_click=increment, type="flat")
    me.button("Decrement", on_click=decrement, type="flat")
