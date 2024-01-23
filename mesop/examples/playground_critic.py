import time

import mesop as me
from mesop.examples.shared.navmenu import scaffold


class Fake:
  def generate_text(self, input: str) -> str:
    # Simulate a slow-ish API call
    time.sleep(2)
    return "Some random text from input: " + input


class Output:
  text: str
  loading: bool


@me.stateclass
class State:
  input: str
  initial_output: Output
  critic_output: Output


@me.page(path="/playground-critic")
def app():
  with scaffold(url="/playground-critic"):
    with me.box(style=me.Style(display="flex", flex_direction="column")):
      header()
      body()


def header():
  with me.box(
    style=me.Style(
      padding=me.Padding(top=12, bottom=12, left=12, right=12),
      border=me.Border(
        bottom=me.BorderSide(width=1, style="solid", color="#ececf1")
      ),
    )
  ):
    me.text(
      "Hello world",
      type="headline-5",
      style=me.Style(margin=me.Margin(top=0, right=0, bottom=0, left=0)),
    )


def body():
  with me.box(
    style=me.Style(
      display="flex",
      flex_grow=1,
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
  state.initial_output.loading = True
  yield
  resp = fake.generate_text(state.input)
  state.initial_output.text = resp
  state.initial_output.loading = False
  state.critic_output.loading = True
  yield
  resp = fake.generate_text("critic: " + resp)
  state.critic_output.text = resp
  state.critic_output.loading = False
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

    with me.box(style=me.Style(margin=me.Margin(top=16, bottom=16))):
      me.divider()
    with me.box(style=me.Style(margin=me.Margin(bottom=8))):
      me.text("Critic prompt", style=me.Style(font_weight=500))

    me.text("Think about something better")


def right_panel():
  with me.box(style=me.Style(width="50%")):
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.text("Output", style=me.Style(font_weight=500))
    state = me.state(State)
    if state.initial_output.loading:
      me.progress_spinner()
    me.text(state.initial_output.text)
    if state.critic_output.loading:
      me.progress_spinner()
    me.text(state.critic_output.text)
