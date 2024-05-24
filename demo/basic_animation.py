import time
from dataclasses import field

import mesop as me


@me.stateclass
class State:
  ex1_rgba: list[int] = field(default_factory=lambda: [255, 0, 0, 1])
  ex2_opacity: float = 1.0
  ex3_width: int
  ex4_left: int


DEFAULT_MARGIN = me.Style(margin=me.Margin.all(30))
BUTTON_MARGIN = me.Style(margin=me.Margin.symmetric(vertical=15))


@me.page(path="/basic_animation")
def app():
  state = me.state(State)

  with me.box(style=DEFAULT_MARGIN):
    me.text("Transform color", type="headline-5")
    me.text(
      "Changing the color can be used to indicate when a field has been updated."
    )
    me.button(
      "Transform",
      type="flat",
      on_click=transform_red_yellow,
      style=BUTTON_MARGIN,
    )
    with me.box(
      style=me.Style(
        background=f"rgba({','.join(map(str, state.ex1_rgba))})",
        width=100,
        height=100,
        margin=me.Margin.all(10),
      )
    ):
      me.text("")

  with me.box(style=DEFAULT_MARGIN):
    me.text("Fade in / Fade out", type="headline-5")
    me.text("Fading in/out can be useful for flash/toast components.")
    me.button(
      "Transform",
      type="flat",
      on_click=transform_fade_in_out,
      style=BUTTON_MARGIN,
    )
    with me.box(
      style=me.Style(
        background="red",
        opacity=state.ex2_opacity,
        width=100,
        height=100,
        margin=me.Margin.all(10),
      )
    ):
      me.text("")

  with me.box(style=DEFAULT_MARGIN):
    me.text("Resize", type="headline-5")
    me.text(
      "Can be used for things like progress bars or opening closing accordion/tabs."
    )
    me.button(
      "Transform", type="flat", on_click=transform_width, style=BUTTON_MARGIN
    )
    with me.box(
      style=me.Style(
        background="rgba(0,0,0,1)",
        width=300,
        height=20,
        margin=me.Margin.all(10),
      )
    ):
      with me.box(
        style=me.Style(
          background="rgba(255, 0, 0, 1)",
          width=str(state.ex3_width) + "%",
          height=20,
        )
      ):
        me.text("")

  with me.box(style=DEFAULT_MARGIN):
    me.text("Move", type="headline-5")
    me.text("Can be used for opening and closing sidebars.")
    me.button(
      "Transform", type="flat", on_click=transform_margin, style=BUTTON_MARGIN
    )
    with me.box():
      with me.box(
        style=me.Style(
          position="relative",
          background="rgba(255, 0, 0, 1)",
          left=state.ex4_left,
          width=30,
          height=30,
        )
      ):
        me.text("")


def transform_red_yellow(e: me.ClickEvent):
  """Transform the color from red to yellow or yellow to red."""
  state = me.state(State)

  if state.ex1_rgba[1] == 0:
    while state.ex1_rgba[1] < 255:
      state.ex1_rgba[1] += 10
      yield
      time.sleep(0.1)
    state.ex1_rgba[1] = 255
    yield
  else:
    while state.ex1_rgba[1] > 0:
      state.ex1_rgba[1] -= 10
      yield
      time.sleep(0.1)
    state.ex1_rgba[1] = 0
    yield


def transform_fade_in_out(e: me.ClickEvent):
  """Update opacity"""
  state = me.state(State)
  if state.ex2_opacity == 0:
    while state.ex2_opacity < 1:
      state.ex2_opacity += 0.05
      yield
      time.sleep(0.1)
    state.ex2_opacity = 1.0
    yield
  else:
    while state.ex2_opacity > 0:
      state.ex2_opacity -= 0.05
      yield
      time.sleep(0.1)
    state.ex2_opacity = 0
    yield


def transform_width(e: me.ClickEvent):
  """Update the width by percentage."""
  state = me.state(State)
  if state.ex3_width == 0:
    while state.ex3_width < 100:
      state.ex3_width += 5
      yield
      time.sleep(0.1)
    state.ex3_width = 100
    yield
  else:
    while state.ex3_width > 0:
      state.ex3_width -= 5
      yield
      time.sleep(0.1)
    state.ex3_width = 0
    yield


def transform_margin(e: me.ClickEvent):
  """Update the position to create sense of movement."""
  state = me.state(State)
  if state.ex4_left == 0:
    while state.ex4_left < 200:
      state.ex4_left += 10
      yield
      time.sleep(0.1)
    state.ex4_left = 200
    yield
  else:
    while state.ex4_left > 0:
      state.ex4_left -= 10
      yield
      time.sleep(0.1)
    state.ex4_left = 0
    yield
