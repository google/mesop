import mesop as me


@me.stateclass
class State:
  input: str = ""
  input_value_when_button_clicked: str


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


def click_button(e: me.ClickEvent):
  state = me.state(State)
  state.input_value_when_button_clicked = state.input


@me.page(path="/components/input/e2e/input_blur_app")
def app():
  s = me.state(State)
  me.input(label="Input", on_blur=on_blur)
  me.button("button", on_click=click_button)
  me.text("Input: " + s.input)
  me.text(
    "input_value_when_button_clicked: " + s.input_value_when_button_clicked
  )

  me.textarea(label="Regular textarea", on_blur=on_blur, value="hello world")

  me.native_textarea(on_blur=on_blur)
