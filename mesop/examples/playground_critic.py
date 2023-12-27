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
      "Playground Critic",
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

    with me.button(type="stroked", on_click=on_submit):
      me.text("Submit")

    with me.box(style="margin: 16px 0"):
      me.divider()
    with me.box(style="margin-bottom: 8px;"):
      me.text("Critic prompt", style="font-weight: 500")

    me.text(
      "Look at the previous output and decide whether there's a better response"
    )


def right_panel():
  with me.box(
    style="""
    width: 50%;
    """
  ):
    with me.box(style="padding-bottom: 16px;"):
      me.text("Output", style="font-weight: 500;")
    state = me.state(State)
    if state.initial_output.loading:
      me.progress_spinner()
    me.text(state.initial_output.text)
    if state.critic_output.loading:
      me.progress_spinner()
    me.text(state.critic_output.text)
