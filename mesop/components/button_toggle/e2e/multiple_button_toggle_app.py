from dataclasses import field

import mesop as me


@me.stateclass
class State:
  selected_values: list[str] = field(
    default_factory=lambda: ["bold", "underline"]
  )


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load, path="/components/button_toggle/e2e/multiple_button_toggle_app"
)
def app():
  state = me.state(State)

  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.button_toggle(
      value=state.selected_values,
      buttons=[
        me.ButtonToggleButton(label="Bold", value="bold"),
        me.ButtonToggleButton(label="Italic", value="italic"),
        me.ButtonToggleButton(label="Underline", value="underline"),
      ],
      multiple=True,
      hide_selection_indicator=False,
      disabled=False,
      on_change=on_change,
      style=me.Style(margin=me.Margin(bottom=20)),
    )

    me.text("Select buttons: " + " ".join(state.selected_values))


def on_change(e: me.ButtonToggleChangeEvent):
  state = me.state(State)
  state.selected_values = e.values
