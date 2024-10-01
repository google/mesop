import mesop as me


@me.stateclass
class State:
  input: str = ""


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/input",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    s = me.state(State)
    me.input(label="Basic input", on_blur=on_blur)
    me.text(text=s.input)
