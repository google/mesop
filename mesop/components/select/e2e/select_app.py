import mesop as me


@me.stateclass
class State:
  selected_value: str = ""


def on_selection_change(e: me.SelectSelectionChangeEvent):
  s = me.state(State)
  s.selected_value = e.value


@me.page(path="/components/select/e2e/select_app")
def app():
  me.text(text="Select")
  me.select(
    label="Select",
    options=[
      me.SelectOption(label="label 1", value="value1"),
      me.SelectOption(label="label 2", value="value2"),
      me.SelectOption(label="label 3", value="value3"),
    ],
    on_selection_change=on_selection_change,
    style=me.Style(width=500),
  )
  s = me.state(State)
  me.text(text="Selected value: " + s.selected_value)
