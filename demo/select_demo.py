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


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/select_demo",
)
def app():
  state = me.state(State)
  with me.box(style=me.Style(margin=me.Margin.all(15))):
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
      appearance="outline",
      value=state.selected_values,
    )
    me.text(text="Selected values: " + ", ".join(state.selected_values))
