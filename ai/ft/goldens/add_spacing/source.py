import mesop as me


@me.stateclass
class State:
  prompt: str
  output: str


def on_prompt_input(event: me.InputEvent):
  state = me.state(State)
  state.prompt = event.value


def on_submit(event: me.ClickEvent):
  state = me.state(State)
  # state.output = api_call(state.prompt)
  state.output = "output: " + state.prompt


@me.page(path="/readme_app")
def app():
  me.text("Hello, world!")
  me.textarea(rows=10, label="Prompt", on_input=on_prompt_input)

  me.button("submit", on_click=on_submit)

  state = me.state(State)
  me.text(f"Output: {state.output}")
