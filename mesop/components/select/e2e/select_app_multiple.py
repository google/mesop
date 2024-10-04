from dataclasses import field

import mesop as me


@me.stateclass
class State:
  selected_values: list[str] = field(
    default_factory=lambda: ["value1", "value3"]
  )


def on_selection_change(e: me.SelectSelectionChangeEvent):
  s = me.state(State)
  s.selected_values = e.values


@me.page(path="/components/select/e2e/select_app_multiple")
def app():
  state = me.state(State)
  me.select(
    label="Select",
    value=state.selected_values,
    options=[
      me.SelectOption(label="label 1", value="value1"),
      me.SelectOption(label="label 2", value="value2"),
      me.SelectOption(label="label 3", value="value3"),
    ],
    on_selection_change=on_selection_change,
    multiple=True,
    style=me.Style(width=500),
  )

  me.text(text="Selected values: " + ", ".join(state.selected_values))
