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
  with me.box(style=me.Style(padding=me.Padding.all(24), max_width=600, margin=me.Margin.symmetric(horizontal="auto"))):
    me.text("Welcome to the README App", style=me.Style(font_size=24, margin=me.Margin(bottom=16)))
    
    me.textarea(rows=10, label="Enter your prompt", on_input=on_prompt_input, style=me.Style(width="100%", margin=me.Margin(bottom=16)))

    me.button("Submit", on_click=on_submit, style=me.Style(margin=me.Margin(bottom=16)))

    state = me.state(State)
    if state.output:
      with me.box(style=me.Style(
        background=me.theme_var("surface"),
        padding=me.Padding.all(16),
        border_radius=8
      )):
        me.text("Output:", style=me.Style(font_weight="bold", margin=me.Margin(bottom=8)))
        me.text(state.output)
