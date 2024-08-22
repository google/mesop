from dataclasses import field

import mesop as me


@me.stateclass
class State:
  data: set = field(default_factory=set)


@me.page(
  path="/testing/set_serialize",
  title="Set Serialize",
)
def app():
  state = me.state(State)
  with me.box(style=me.Style(margin=me.Margin.all(15), display="flex", gap=15)):
    me.button("Init set", type="flat", on_click=on_init_set)
    me.button("Update set", type="flat", on_click=on_update_set)
    me.text("Set values: " + str(sorted(state.data)))
    me.text("Is set: " + str(type(state.data) is set))


def on_init_set(e: me.ClickEvent):
  state = me.state(State)
  state.data = {1, 2, 3}


def on_update_set(e: me.ClickEvent):
  state = me.state(State)
  state.data.add(4)
