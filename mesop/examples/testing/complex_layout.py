"""Page for smoke testing component diffing."""

import mesop as me


@me.stateclass
class State:
  color1: str = "red"
  color2: str = "orange"
  color3: str = "yellow"
  color4: str = "green"
  color5: str = "blue"
  color6: str = "indigo"
  color7: str = "violet"
  random_inputs: bool = False
  other_random_inputs: bool = False


@me.page(path="/testing/complex_layout")
def app():
  state = me.state(State)

  # Test general diff updates
  me.button("Reverse colors", on_click=update_colors)
  # Test diff propagation
  me.button("Update last color", on_click=update_last_color)
  # Test adding components to differents parts of tree
  me.button("Show random inputs", on_click=show_random_inputs)
  # Test replacement of components to differenet components
  me.button("Show other random inputs", on_click=show_other_random_inputs)
  # Test deletion of components
  me.button("Hide random inputs", on_click=hide_random_inputs)

  with me.box(
    key="box1",
    style=me.Style(background=state.color1, padding=me.Padding.all(10)),
  ):
    me.text("Label " + state.color1)
    with me.box(
      style=me.Style(background=state.color2, padding=me.Padding.all(10))
    ):
      me.text("Label " + state.color2)
      with me.box(
        style=me.Style(background=state.color3, padding=me.Padding.all(10))
      ):
        me.text("Label " + state.color3)
        if state.random_inputs:
          with me.box(
            style=me.Style(border=me.Border.all(me.BorderSide(width=1)))
          ):
            me.checkbox(state.color3)
            me.input(label=state.color3)
            me.radio(
              options=[
                me.RadioOption(label="Radio 1"),
                me.RadioOption(label="Radio 2"),
              ]
            )
            me.slider()
        if state.other_random_inputs:
          with me.box(
            style=me.Style(border=me.Border.all(me.BorderSide(width=1)))
          ):
            me.checkbox(state.color3)
            me.radio(
              options=[
                me.RadioOption(label="Radio 1"),
                me.RadioOption(label="Radio 2"),
              ]
            )
            me.input(label=state.color3)
        with me.box(
          style=me.Style(background=state.color4, padding=me.Padding.all(10))
        ):
          me.text("Label " + state.color4)
          with me.box(
            style=me.Style(background=state.color5, padding=me.Padding.all(10))
          ):
            me.text("Label " + state.color5)
            with me.box(
              style=me.Style(
                background=state.color6, padding=me.Padding.all(10)
              )
            ):
              me.text("Label " + state.color6)
              with me.box(
                style=me.Style(
                  background=state.color7, padding=me.Padding.all(10)
                )
              ):
                me.text("Label " + state.color7)
                if state.random_inputs:
                  me.input(label=state.color7)
                  me.checkbox(state.color7)
                  me.slider()
                  me.radio(
                    options=[
                      me.RadioOption(label="Radio 1"),
                      me.RadioOption(label="Radio 2"),
                    ]
                  )
                if state.other_random_inputs:
                  me.checkbox(state.color7)
                  me.input(label=state.color7)
                  me.radio(options=[me.RadioOption(label="Radio 2")])


def update_colors(e: me.ClickEvent):
  state = me.state(State)
  if state.color7 == "red":
    state.color1 = "red"
    state.color2 = "orange"
    state.color3 = "yellow"
    state.color4 = "green"
    state.color5 = "blue"
    state.color6 = "indigo"
    state.color7 = "violet"
  else:
    state.color7 = "red"
    state.color6 = "orange"
    state.color5 = "yellow"
    state.color4 = "green"
    state.color3 = "blue"
    state.color2 = "indigo"
    state.color1 = "violet"


def update_last_color(e: me.ClickEvent):
  state = me.state(State)
  state.color7 = "white"


def show_random_inputs(e: me.ClickEvent):
  state = me.state(State)
  state.random_inputs = True
  state.other_random_inputs = False


def show_other_random_inputs(e: me.ClickEvent):
  state = me.state(State)
  state.other_random_inputs = True
  state.random_inputs = False


def hide_random_inputs(e: me.ClickEvent):
  state = me.state(State)
  state.random_inputs = False
  state.other_random_inputs = False
