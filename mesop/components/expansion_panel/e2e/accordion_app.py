from dataclasses import field

import mesop as me


@me.stateclass
class State:
  normal_accordion: dict[str, bool] = field(
    default_factory=lambda: {"pie": True, "donut": False, "icecream": False}
  )


@me.page(
  path="/components/expansion_panel/e2e/accordion_app",
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
    me.text("Normal Accordion", type="headline-5")
    with me.accordion():
      with me.expansion_panel(
        key="pie",
        title="Pie title",
        description="Type of snack",
        icon="pie_chart",
        disabled=False,
        expanded=state.normal_accordion["pie"],
        hide_toggle=False,
        on_toggle=on_accordion_toggle,
      ):
        me.text("Pie content.")

      with me.expansion_panel(
        key="donut",
        title="Donut title",
        description="Type of breakfast",
        icon="donut_large",
        disabled=False,
        expanded=state.normal_accordion["donut"],
        hide_toggle=False,
        on_toggle=on_accordion_toggle,
      ):
        me.text("Donut content.")

      with me.expansion_panel(
        key="icecream",
        title="Ice cream title",
        description="Type of dessert",
        icon="icecream",
        disabled=False,
        expanded=state.normal_accordion["icecream"],
        hide_toggle=False,
        on_toggle=on_accordion_toggle,
      ):
        me.text("Ice cream content.")


def on_accordion_toggle(e: me.ExpansionPanelToggleEvent):
  """Implements accordion behavior where only one panel can be open at a time"""
  state = me.state(State)
  state.normal_accordion = {"pie": False, "donut": False, "icecream": False}
  state.normal_accordion[e.key] = e.opened
