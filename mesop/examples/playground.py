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
    with me.box(
      style="""
      display: flex;
      flex-direction: column;
      """
    ):
      header()
      body()


def header():
  with me.box(
    style="""
  border-bottom: 1px solid #ececf1;
  padding: 12px;
  """
  ):
    me.text(
      "Playground",
      type=me.Typography.H5,
      style="""
    margin: 0;
    """,
    )


def body():
  with me.box(
    style="""
    flex-grow: 1;
    padding: 24px;
    display: flex;
    flex-direction: row;
  """
  ):
    left_panel()
    with me.box(style="width: 24px"):
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
    style="""
    display: flex:
    flex-direction: column;
    width: 50%;
    """
  ):
    with me.box(style="padding-bottom: 16px;"):
      me.text("Input", style="font-weight: 500;")
    with me.box(style="""width: 100%;"""):
      me.input(
        label="Input",
        type=me.Textarea(rows=10),
        style="width: 100%",
        on_input=on_input,
      )

    with me.button(variant="stroked", on_click=on_submit):
      me.text("Submit")


def right_panel():
  with me.box(
    style="""
    width: 50%;
    """
  ):
    with me.box(style="padding-bottom: 16px;"):
      me.text("Output", style="font-weight: 500;")
    state = me.state(State)
    if state.is_loading:
      me.progress_spinner(diameter=48, stroke_width=4, mode="indeterminate")
    me.text(state.response)
