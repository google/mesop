import mesop as me


@me.stateclass
class State:
  input: str = ""


def on_input(e: me.InputEvent):
  state = me.state(State)
  state.input = e.value


@me.page(path="/components/input/e2e/input_app")
def app():
  s = me.state(State)
  me.input(label="Basic input", on_input=on_input)
  me.text(text=s.input)

  me.textarea(
    label="Textarea", on_input=on_input, value="hello world", color="warn"
  )
  me.input(
    label="Number input", type="number", on_input=on_input, color="accent"
  )
  me.markdown("# Native input")
  border_side = me.BorderSide(width=0)
  with me.box(
    style=me.Style(
      background="lightblue",
      padding=me.Padding(
        top=16,
        left=16,
        right=16,
        bottom=16,
      ),
    )
  ):
    me.native_textarea(
      readonly=False,
      style=me.Style(
        height=32,
        padding=me.Padding(top=16, right=16, bottom=16, left=16),
        border_radius=16,
        border=me.Border(
          top=border_side,
          right=border_side,
          bottom=border_side,
          left=border_side,
        ),
        outline="none",
      ),
    )
