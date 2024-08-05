"""Simple snackbar component that is similar to Angular Component Snackbar."""

import time
from typing import Callable, Literal

import mesop as me


@me.stateclass
class State:
  is_visible: bool = False
  duration: int = 0
  horizontal_position: str = "center"
  vertical_position: str = "end"


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/snackbar",
)
def app():
  me.set_theme_mode("dark")
  state = me.state(State)

  snackbar(
    label="Cannonball!!!",
    action_label="Splash",
    on_click_action=on_click_snackbar_close,
    is_visible=state.is_visible,
    horizontal_position=state.horizontal_position,  # type: ignore
    vertical_position=state.vertical_position,  # type: ignore
  )

  with me.box(style=me.Style(padding=me.Padding.all(30))):
    with me.box():
      me.select(
        label="Horizontal Position",
        on_selection_change=on_horizontal_position_change,
        options=[
          me.SelectOption(label="start", value="start"),
          me.SelectOption(label="center", value="center"),
          me.SelectOption(label="end", value="end"),
        ],
      )

    with me.box():
      me.select(
        label="Vertical Position",
        on_selection_change=on_vertical_position_change,
        options=[
          me.SelectOption(label="start", value="start"),
          me.SelectOption(label="center", value="center"),
          me.SelectOption(label="end", value="end"),
        ],
      )

    with me.box():
      me.select(
        label="Duration",
        on_selection_change=on_duration_change,
        options=[
          me.SelectOption(label="None", value="0"),
          me.SelectOption(label="3 seconds", value="3"),
        ],
      )

    me.button(
      "Trigger snackbar",
      type="flat",
      color="primary",
      on_click=on_click_snackbar_open,
    )


def on_horizontal_position_change(e: me.SelectSelectionChangeEvent):
  state = me.state(State)
  state.horizontal_position = e.value


def on_vertical_position_change(e: me.SelectSelectionChangeEvent):
  state = me.state(State)
  state.vertical_position = e.value


def on_duration_change(e: me.SelectSelectionChangeEvent):
  state = me.state(State)
  state.duration = int(e.value)


def on_click_snackbar_close(e: me.ClickEvent):
  state = me.state(State)
  state.is_visible = False


def on_click_snackbar_open(e: me.ClickEvent):
  state = me.state(State)
  state.is_visible = True

  # Use yield to create a timed snackbar message.
  if state.duration:
    yield
    time.sleep(state.duration)
    state.is_visible = False
    yield
  else:
    yield


@me.component
def snackbar(
  *,
  is_visible: bool,
  label: str,
  action_label: str | None = None,
  on_click_action: Callable | None = None,
  horizontal_position: Literal["start", "center", "end"] = "center",
  vertical_position: Literal["start", "center", "end"] = "end",
):
  """Creates a snackbar.

  By default the snackbar is rendered at bottom center.

  The on_click_action should typically close the snackbar as part of its actions. If no
  click event is included, you'll need to manually hide the snackbar.

  Note that there is one issue with this snackbar example. No actions are possible when
  using "time.sleep and yield" to imitate a status message that fades away after a
  period of time.

  Args:
    is_visible: Whether the snackbar is currently visible or not.
    label: Message for the snackbar
    action_label: Optional message for the action of the snackbar
    on_click_action: Optional click event when action is triggered.
    horizontal_position: Horizontal position of the snackbar
    vertical_position: Vertical position of the snackbar
  """
  with me.box(
    style=me.Style(
      display="block" if is_visible else "none",
      height="100%",
      overflow_x="auto",
      overflow_y="auto",
      position="fixed",
      pointer_events="none",
      width="100%",
      z_index=1000,
    )
  ):
    with me.box(
      style=me.Style(
        align_items=vertical_position,
        height="100%",
        display="flex",
        justify_content=horizontal_position,
      )
    ):
      with me.box(
        style=me.Style(
          align_items="center",
          background=me.theme_var("on-surface-variant"),
          border_radius=5,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          display="flex",
          font_size=14,
          justify_content="space-between",
          margin=me.Margin.all(10),
          padding=me.Padding(top=5, bottom=5, right=5, left=15)
          if action_label
          else me.Padding.all(15),
          pointer_events="auto",
          width=300,
        )
      ):
        me.text(
          label, style=me.Style(color=me.theme_var("surface-container-lowest"))
        )
        if action_label:
          me.button(
            action_label,
            on_click=on_click_action,
            style=me.Style(color=me.theme_var("primary-container")),
          )
