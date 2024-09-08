import mesop as me


@me.stateclass
class State:
  input: str = ""
  output: str = ""


def on_prompt_click(e: me.ClickEvent):
  state = me.state(State)
  state.input = e.key


def on_submit(e: me.ClickEvent):
  state = me.state(State)
  if state.input == "Hello!":
    state.output = "Hello there!"
  elif state.input == "How are you?":
    state.output = "I'm doing well, thank you!"
  elif state.input == "What's the weather like?":
    state.output = "It's sunny outside."
  elif state.input == "Tell me a joke.":
    state.output = (
      "Why don't scientists trust atoms? Because they make up everything!"
    )


@me.page(path="/box")
def app():
  state = me.state(State)
  with me.box(
    style=me.Style(
      padding=me.Padding.all(24),
      border_radius=12,
      background=me.theme_var("background"),
      box_shadow="0 4px 8px rgba(0,0,0,0.1)",
    )
  ):
    with me.box(
      style=me.Style(
        margin=me.Margin(bottom=24), display="flex", gap=12, flex_wrap="wrap"
      )
    ):
      prompts = [
        "Hello!",
        "How are you?",
        "What's the weather like?",
        "Tell me a joke.",
      ]
      for prompt in prompts:
        me.button(
          prompt,
          key=prompt,
          on_click=on_prompt_click,
          type="flat",
          style=me.Style(
            border_radius=8,
            background=me.theme_var("surface-container"),
            color=me.theme_var("on-surface"),
          ),
        )
    with me.box(
      style=me.Style(display="flex", gap=12, flex_direction="column")
    ):
      me.input(
        label="Chat input",
        value=state.input,
        style=me.Style(
          border_radius=8,
          width="100%",
          background=me.theme_var("surface-container"),
          color=me.theme_var("on-surface"),
        ),
      )
      me.button(
        "Submit",
        on_click=on_submit,
        type="flat",
        style=me.Style(
          border_radius=8,
          background=me.theme_var("primary"),
          color=me.theme_var("on-primary"),
        ),
      )
      if state.output:
        me.text(
          state.output,
          style=me.Style(font_weight=500, color=me.theme_var("primary")),
        )
