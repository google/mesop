"""Simple modal that looks similar to Angular Component Dialog."""

import mesop as me


@me.stateclass
class State:
  is_open: bool = False


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/modal",
)
def app():
  state = me.state(State)

  with modal(state.is_open):
    with modal_container():
      me.text("Delete File", type="headline-5")
      with me.box():
        me.text(text="Would you like to delete cat.jpeg?")
      with modal_actions():
        me.button("No", on_click=on_click_close_modal)
        me.button("Yes", on_click=on_click_close_modal)

  with me.box(style=me.Style(padding=me.Padding.all(30))):
    me.button(
      "Open Modal", type="flat", color="primary", on_click=on_click_modal_open
    )


def on_click_close_modal(e: me.ClickEvent):
  state = me.state(State)
  state.is_open = False


def on_click_modal_open(e: me.ClickEvent):
  state = me.state(State)
  state.is_open = True


@me.content_component
def modal(is_open: bool):
  """Renders the background container that will host the modal.

  One current drawback is that it's not possible to close the modal
  by clicking on the overlay background. This is due to
  https://github.com/google/mesop/issues/268.

  Args:
    is_open: Whether the modal is visible or not.
  """
  with me.box(
    style=me.Style(
      background="rgba(0,0,0,0.4)",
      display="block" if is_open else "none",
      height="100%",
      overflow_x="auto",
      overflow_y="auto",
      position="fixed",
      width="100%",
      z_index=1000,
    )
  ):
    with me.box(
      style=me.Style(
        align_items="center",
        display="grid",
        height="100vh",
        justify_items="center",
      )
    ):
      me.slot()


@me.content_component
def modal_container():
  """Helper component for rendering modal itself.

  The design of the modal borrows from the Angular component dialog. So basically
  rounded corners and some box shadow.
  """
  with me.box(
    style=me.Style(
      background="#fff",
      border_radius=20,
      box_sizing="content-box",
      box_shadow=(
        "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
      ),
      margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
      padding=me.Padding.all(20),
    )
  ):
    me.slot()


@me.content_component
def modal_actions():
  """Helper component for rendering action buttons so they are right aligned.

  This component is optional. If you want to position action buttons differently,
  you can just write your own Mesop markup.
  """
  with me.box(
    style=me.Style(
      display="flex", justify_content="end", margin=me.Margin(top=20)
    )
  ):
    me.slot()
