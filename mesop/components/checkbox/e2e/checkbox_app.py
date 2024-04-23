import mesop as me


@me.stateclass
class State:
  checked: bool = True
  indeterminate: bool = True


def on_update(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checked = event.checked


@me.page(path="/components/checkbox/e2e/checkbox_app")
def app():
  state = me.state(State)
  me.checkbox(
    "label",
    on_change=on_update,
    checked=state.checked,
    disable_ripple=False,
    indeterminate=False,
    style=me.Style(
      border=me.Border.all(
        me.BorderSide(
          width=1,
          color="green",
          style="solid",
        )
      )
    ),
  )

  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
