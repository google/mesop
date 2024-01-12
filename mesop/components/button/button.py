from typing import Any, Callable, Literal

import mesop.components.button.button_pb2 as button_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_component,
  register_event_handler,
)
from mesop.events import ClickEvent


@register_component
def button(
  *,
  on_click: Callable[[ClickEvent], Any] | None = None,
  type: Literal["raised", "flat", "stroked", "icon"] | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  disable_ripple: bool = False,
  disabled: bool = False,
  key: str | None = None,
):
  """Creates a Button component.
  Button is a composite component.

  Args:
    on_click: [click](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/click_event) is a native browser event.
    type: Type of button style to use
    color: Theme color palette of the button
    disable_ripple: Whether the ripple effect is disabled or not.
    disabled: Whether the button is disabled.
    key: Unique identifier for this component instance.
  """
  return insert_composite_component(
    key=key,
    type_name="button",
    proto=button_pb.ButtonType(
      color=color,
      disable_ripple=disable_ripple,
      disabled=disabled,
      on_click_handler_id=register_event_handler(on_click, event=ClickEvent)
      if on_click
      else "",
      type_index=_get_type_index(type),
      type=type,
    ),
  )


def _get_type_index(
  type: Literal["raised", "flat", "stroked", "icon"] | None,
) -> int:
  if type is None:
    return 0
  if type == "raised":
    return 1
  if type == "flat":
    return 2
  if type == "stroked":
    return 3
  if type == "icon":
    return 4
  raise Exception("Unexpected type: " + type)
