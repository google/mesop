import mesop as me


@me.stateclass
class State:
  opened: bool = False


@me.page(path="/components/expansion_panel/e2e/expansion_panel_app")
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
    with me.expansion_panel(
      title="Grapefruit title",
      description="Type of fruit",
      icon="nutrition",
      disabled=False,
      hide_toggle=False,
      expanded=state.opened,
      on_toggle=on_toggle,
    ):
      me.text("Grapefruit content.")

    with me.expansion_panel(
      title="Pineapple title",
      icon="nutrition",
      disabled=True,
      hide_toggle=False,
    ):
      me.text("Pineapple content.")

    with me.expansion_panel(
      title="Cantalope (no description)",
      hide_toggle=True,
    ):
      me.text("Cantalope content.")


def on_toggle(e: me.ExpansionPanelToggleEvent):
  me.state(State).opened = e.opened
