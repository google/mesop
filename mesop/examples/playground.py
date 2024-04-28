import time

import mesop as me
from mesop.examples.shared.navmenu import scaffold


class Fake:
  def generate_text(self, input: str) -> str:
    # Simulate a slow-ish API call
    time.sleep(2)
    return "Some random text from input: " + input


@me.stateclass
class State:
  input: str = ""
  response: str = ""
  is_loading: bool = False


@me.page(path="/playground")
def app():
  with scaffold(url="/playground"):
    with me.box(style=me.Style(display="flex", flex_direction="column")):
      header()
      body()


def header():
  with me.box(
    style=me.Style(
      padding=me.Padding(left=12, right=12, top=12, bottom=12),
      border=me.Border(
        bottom=me.BorderSide(width=1, style="solid", color="#ececf1")
      ),
    )
  ):
    me.text(
      "Playground Page",
      type="headline-5",
      style=me.Style(margin=me.Margin(top=0, right=0, bottom=0, left=0)),
    )


def body():
  with me.box(
    style=me.Style(
      flex_grow=1,
      display="flex",
      flex_direction="row",
      padding=me.Padding(top=24, bottom=24, left=24, right=24),
    )
  ):
    left_panel()
    with me.box(style=me.Style(width=24)):
      pass
    right_panel()


def on_input(e: me.InputEvent):
  me.state(State).input = e.value


def on_submit(event: me.ClickEvent):
  fake = Fake()
  state = me.state(State)
  state.is_loading = True
  yield
  resp = fake.generate_text(state.input)
  state.response = resp
  state.is_loading = False
  yield


def left_panel():
  with me.box(
    style=me.Style(display="flex", flex_direction="column", width="50%")
  ):
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.text("Input", style=me.Style(font_weight=500))
    with me.box(style=me.Style(width="100%")):
      me.textarea(
        label="Input",
        rows=10,
        style=me.Style(width="100%"),
        on_input=on_input,
      )

    me.button("Submit", type="stroked", on_click=on_submit)


def right_panel():
  with me.box(style=me.Style(width="50%")):
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.text("Output", style=me.Style(font_weight=500))
    state = me.state(State)
    if state.is_loading:
      me.progress_spinner()
    me.text(state.response)
