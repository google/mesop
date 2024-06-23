import mesop as me


@me.stateclass
class State:
  selected_values: list[str]


def on_selection_change(e: me.SelectSelectionChangeEvent):
  s = me.state(State)
  s.selected_values = e.values


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/select_demo",
)
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
    multiple=True,
  )
  s = me.state(State)
  me.text(text="Selected values: " + ", ".join(s.selected_values))
