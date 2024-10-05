import mesop as me


@me.stateclass
class State:
  selected_value: str = "bold"


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load, path="/components/button_toggle/e2e/single_button_toggle_app"
)
def app():
  state = me.state(State)

  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.button_toggle(
      value=state.selected_value,
      buttons=[
        me.ButtonToggleButton(label="Bold", value="bold"),
        me.ButtonToggleButton(label="Italic", value="italic"),
        me.ButtonToggleButton(label="Underline", value="underline"),
      ],
      multiple=False,
      hide_selection_indicator=False,
      disabled=False,
      on_change=on_change,
      style=me.Style(margin=me.Margin(bottom=20)),
    )

    me.text("Select button: " + " ".join(state.selected_value))


def on_change(e: me.ButtonToggleChangeEvent):
  state = me.state(State)
  state.selected_value = e.value
