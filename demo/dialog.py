"""Simple dialog that looks similar to Angular Component Dialog."""

from typing import Callable

import mesop as me


@me.stateclass
class State:
  is_open: bool = False


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/dialog",
)
def app():
  state = me.state(State)

  with dialog(
    is_open=state.is_open,
    on_click_background=on_click_close_background,
  ):
    me.text("Delete File", type="headline-5")
    with me.box():
      me.text(text="Would you like to delete cat.jpeg?")
    with dialog_actions():
      me.button("No", on_click=on_click_close_dialog)
      me.button("Yes", on_click=on_click_close_dialog)

  with me.box(style=me.Style(padding=me.Padding.all(30))):
    me.button(
      "Open Dialog", type="flat", color="primary", on_click=on_click_dialog_open
    )


def on_click_close_background(e: me.ClickEvent):
  state = me.state(State)
  if e.is_target:
    state.is_open = False


def on_click_close_dialog(e: me.ClickEvent):
  state = me.state(State)
  state.is_open = False


def on_click_dialog_open(e: me.ClickEvent):
  state = me.state(State)
  state.is_open = True


@me.content_component
def dialog(*, is_open: bool, on_click_background: Callable | None = None):
  """Renders a dialog component.

  The design of the dialog borrows from the Angular component dialog. So basically
  rounded corners and some box shadow.

  Args:
    is_open: Whether the dialog is visible or not.
    on_click_background: Event handler for when background is clicked
  """
  with me.box(
    style=me.Style(
      background="rgba(0, 0, 0, 0.4)"
      if me.theme_brightness() == "light"
      else "rgba(255, 255, 255, 0.4)",
      display="block" if is_open else "none",
      height="100%",
      overflow_x="auto",
      overflow_y="auto",
      position="fixed",
      width="100%",
      z_index=1000,
    ),
  ):
    with me.box(
      on_click=on_click_background,
      style=me.Style(
        place_items="center",
        display="grid",
        height="100vh",
      ),
    ):
      with me.box(
        style=me.Style(
          background=me.theme_var("surface-container-lowest"),
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
def dialog_actions():
  """Helper component for rendering action buttons so they are right aligned.

  This component is optional. If you want to position action buttons differently,
  you can just write your own Mesop markup.
  """
  with me.box(
    style=me.Style(
      display="flex", justify_content="end", gap=5, margin=me.Margin(top=20)
    )
  ):
    me.slot()
