import time

import mesop as me


@me.stateclass
class State:
  ex1_rgba: list[int]
  ex2_rgba: list[int]
  ex3_width: int
  ex4_margin: int


DEFAULT_MARGIN = me.Style(margin=me.Margin.all(30))
BUTTON_MARGIN = me.Style(margin=me.Margin.symmetric(vertical=15))


@me.page(path="/basic_animation")
def app():
  state = me.state(State)

  # Initialize default values
  if not state.ex1_rgba:
    state.ex1_rgba = [255, 0, 0, 1]
    state.ex2_rgba = [255, 0, 0, 1]

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
        background=f"rgba({','.join(map(str, state.ex2_rgba))})",
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
    with me.box(
      style=me.Style(
        background="rgba(255, 0, 0, 1)",
        margin=me.Margin(left=state.ex4_margin, top=20),
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
  """Update alpha of the rgba.

  The better option would be to use opacity, but Mesop does not have that property
  available yet.
  """
  state = me.state(State)
  if state.ex2_rgba[3] == 0:
    while state.ex2_rgba[3] < 1:
      state.ex2_rgba[3] += 0.05
      yield
      time.sleep(0.1)
    state.ex2_rgba[3] = 1
    yield
  else:
    while state.ex2_rgba[3] > 0:
      state.ex2_rgba[3] -= 0.05
      yield
      time.sleep(0.1)
    state.ex2_rgba[3] = 0
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
  """Update the margin to create sense of movement.

  Mesop does not yet have the top/bottom/left/right properties available,
  so just modifying the margin for this example.
  """
  state = me.state(State)
  if state.ex4_margin == 0:
    while state.ex4_margin < 200:
      state.ex4_margin += 10
      yield
      time.sleep(0.1)
    state.ex4_margin = 200
    yield
  else:
    while state.ex4_margin > 0:
      state.ex4_margin -= 10
      yield
      time.sleep(0.1)
    state.ex4_margin = 0
    yield
