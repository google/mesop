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
  me.input(type=me.Textarea(rows=10), label="Prompt", on_input=on_prompt_input)

  with me.button(on_click=on_submit):
    me.text("Submit")

  state = me.state(State)
  me.text(f"Output: {state.output}")
