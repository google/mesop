import mesop as me


@me.stateclass
class State:
  inner_counter: int = 0
  outer_counter: int = 0


@me.page(path="/components/box/e2e/box_app")
def app():
  state = me.state(State)
  me.text(f"Outer counter: {state.outer_counter}")
  me.text(f"Inner counter: {state.inner_counter}")
  with me.box(
    style=me.Style(background="red", padding=me.Padding.all(16)),
    on_click=on_outer_click,
  ):
    me.text(text="outer-box")
    with me.box(
      style=me.Style(
        background="green",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          horizontal=me.BorderSide(width=2, color="pink", style="solid"),
          vertical=me.BorderSide(width=2, color="orange", style="solid"),
        ),
      ),
      on_click=on_inner_click,
    ):
      me.text(text="inner-box")


def on_outer_click(e: me.ClickEvent):
  state = me.state(State)
  state.outer_counter += 1


def on_inner_click(e: me.ClickEvent):
  state = me.state(State)
  state.inner_counter += 1
