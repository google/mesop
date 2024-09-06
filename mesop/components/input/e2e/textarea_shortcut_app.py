import mesop as me


@me.stateclass
class State:
  input: str = ""
  output: str = ""
  shortcut: str = ""


def on_newline(e: me.TextareaShortcutEvent):
  state = me.state(State)
  state.input = e.value + "\n"


def on_submit(e: me.TextareaShortcutEvent):
  state = me.state(State)
  state.input = e.value
  state.output = e.value


def on_shortcut(e: me.TextareaShortcutEvent):
  state = me.state(State)
  state.shortcut = str(e.shortcut)


@me.page(path="/components/input/e2e/textarea_shortcut_app")
def app():
  s = me.state(State)
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.textarea(
      label="Textarea",
      value=s.input,
      shortcuts={
        me.Shortcut(key="enter"): on_submit,
        me.Shortcut(shift=True, key="ENTER"): on_newline,
        me.Shortcut(ctrl=True, alt=True, key="Enter"): on_shortcut,
        me.Shortcut(meta=True, key="S"): on_shortcut,
        me.Shortcut(key="escape"): on_shortcut,
      },
    )

    me.native_textarea(
      placeholder="Native textarea",
      value=s.input,
      autosize=True,
      min_rows=5,
      shortcuts={
        me.Shortcut(key="enter"): on_submit,
        me.Shortcut(shift=True, key="ENTER"): on_newline,
        me.Shortcut(ctrl=True, alt=True, key="Enter"): on_shortcut,
        me.Shortcut(meta=True, key="S"): on_shortcut,
        me.Shortcut(key="escape"): on_shortcut,
      },
    )

    me.text(text="Submitted: " + s.output)
    me.text(text="Shortcut: " + s.shortcut)
