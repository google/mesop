from dataclasses import field

import mesop as me


@me.stateclass
class State:
  selected_values_1: list[str] = field(
    default_factory=lambda: ["value1", "value2"]
  )
  selected_values_2: str = "value1"


def on_selection_change_1(e: me.SelectSelectionChangeEvent):
  s = me.state(State)
  s.selected_values_1 = e.values


def on_selection_change_2(e: me.SelectSelectionChangeEvent):
  s = me.state(State)
  s.selected_values_2 = e.value


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
      label="Select multiple",
      options=[
        me.SelectOption(label="label 1", value="value1"),
        me.SelectOption(label="label 2", value="value2"),
        me.SelectOption(label="label 3", value="value3"),
      ],
      on_selection_change=on_selection_change_1,
      style=me.Style(width=500),
      multiple=True,
      appearance="outline",
      value=state.selected_values_1,
    )
    me.text(
      text="Selected values (multiple): " + ", ".join(state.selected_values_1)
    )

    me.select(
      label="Select single",
      options=[
        me.SelectOption(label="label 1", value="value1"),
        me.SelectOption(label="label 2", value="value2"),
        me.SelectOption(label="label 3", value="value3"),
      ],
      on_selection_change=on_selection_change_2,
      style=me.Style(width=500, margin=me.Margin(top=40)),
      multiple=False,
      appearance="outline",
      value=state.selected_values_2,
    )
    me.text(text="Selected values (single): " + state.selected_values_2)
