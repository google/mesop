import mesop as me


@me.stateclass
class State:
  initial_input_value: str = "50.0"
  initial_slider_value: float = 50.0
  slider_value: float = 50.0


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/slider",
)
def app():
  state = me.state(State)
  with me.box(style=me.Style(display="flex", flex_direction="column", gap=24, padding=me.Padding.all(32))):
    me.text(
      "Slider Sample",
      style=me.Style(
        font_size=24,
        font_weight="bold",
        margin=me.Margin(bottom=16)
      )
  )
    with me.box(style=me.Style(display="flex", align_items="center", gap=16)):
      me.text(
        "Value:",
        style=me.Style(
          font_size=16,
          font_weight=500,
          color=me.theme_var("on-surface")
        )
      )
      me.text(
        f"{state.slider_value:.2f}",
        style=me.Style(
          font_size=16,
          font_weight=500,
          color=me.theme_var("primary"),
          padding=me.Padding.symmetric(horizontal=8),
          border=me.Border.all(me.BorderSide(width=1, color=me.theme_var("outline"))),
          border_radius=4
        )
      )
    me.slider(
      value=state.slider_value,
      on_value_change=on_value_change,
      style=me.Style(
        margin=me.Margin(top=16)
      )
    )
    me.text(
      "Adjust the slider to change the value.",
      style=me.Style(
        font_size=14,
        color=me.theme_var("on-surface-variant"),
        margin=me.Margin(top=8)
      )
    )


def on_value_change(event: me.SliderValueChangeEvent):
  state = me.state(State)
  state.slider_value = event.value
  state.initial_input_value = str(state.slider_value)


def on_input(event: me.InputEvent):
  state = me.state(State)
  state.initial_slider_value = float(event.value)
  state.slider_value = state.initial_slider_value
