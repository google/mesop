import mesop as me


@me.stateclass
class State:
  input: str = ""


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/input",
)
def app():
  s = me.state(State)
  me.input(label="Basic input", on_blur=on_blur)
  me.text(text=s.input)
