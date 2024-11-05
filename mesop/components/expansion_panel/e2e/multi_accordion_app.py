from dataclasses import field

import mesop as me


@me.stateclass
class State:
  multi_accordion: dict[str, bool] = field(
    default_factory=lambda: {"pie": False, "donut": False, "icecream": False}
  )


@me.page(
  path="/components/expansion_panel/e2e/multi_accordion_app",
)
def app():
  state = me.state(State)
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=15,
      margin=me.Margin.all(15),
      max_width=500,
    )
  ):
    with me.box(
      style=me.Style(display="flex", gap=20, margin=me.Margin(bottom=15)),
    ):
      me.button(
        label="Open All", type="flat", on_click=on_multi_accordion_open_all
      )
      me.button(
        label="Close All", type="flat", on_click=on_multi_accordion_close_all
      )

    with me.accordion():
      with me.expansion_panel(
        key="pie",
        title="Pie title",
        description="Type of snack",
        icon="pie_chart",
        expanded=state.multi_accordion["pie"],
        on_toggle=on_multi_accordion_toggle,
      ):
        me.text("Pie content.")

      with me.expansion_panel(
        key="donut",
        title="Donut Title",
        description="Type of breakfast",
        icon="donut_large",
        expanded=state.multi_accordion["donut"],
        on_toggle=on_multi_accordion_toggle,
      ):
        me.text("Donut content.")

      with me.expansion_panel(
        key="icecream",
        title="Ice cream title",
        description="Type of dessert",
        icon="icecream",
        expanded=state.multi_accordion["icecream"],
        on_toggle=on_multi_accordion_toggle,
      ):
        me.text("Ice cream content.")


def on_multi_accordion_toggle(e: me.ExpansionPanelToggleEvent):
  """Implements accordion behavior where multiple panels can be open at a time"""
  state = me.state(State)
  state.multi_accordion[e.key] = e.opened


def on_multi_accordion_open_all(e: me.ClickEvent):
  state = me.state(State)
  for key in state.multi_accordion:
    state.multi_accordion[key] = True


def on_multi_accordion_close_all(e: me.ClickEvent):
  state = me.state(State)
  for key in state.multi_accordion:
    state.multi_accordion[key] = False
