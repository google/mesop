from typing import Any, Callable, Literal

import mesop.components.button.button_pb2 as button_pb
from mesop.component_helpers import (
  Style,
  component,
  insert_composite_component,
  register_event_handler,
  register_native_component,
)
from mesop.components.text.text import text
from mesop.events import ClickEvent


@component
def button(
  label: str | None = None,
  *,
  on_click: Callable[[ClickEvent], Any] | None = None,
  type: Literal["raised", "flat", "stroked"] | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  disable_ripple: bool = False,
  disabled: bool = False,
  style: Style | None = None,
  key: str | None = None,
):
  """Creates a simple text Button component.

  Args:
    label: Text label for button
    on_click: [click](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/click_event) is a native browser event.
    type: Type of button style to use
    color: Theme color palette of the button
    disable_ripple: Whether the ripple effect is disabled or not.
    disabled: Whether the button is disabled.
    style: Style for the component.
    key: The component [key](../components/index.md#component-key).
  """
  with content_button(
    on_click=on_click,
    type=type,
    color=color,
    disable_ripple=disable_ripple,
    disabled=disabled,
    style=style,
    key=key,
  ):
    text(label)


@register_native_component
def content_button(
  *,
  on_click: Callable[[ClickEvent], Any] | None = None,
  type: Literal["raised", "flat", "stroked", "icon"] | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  disable_ripple: bool = False,
  disabled: bool = False,
  style: Style | None = None,
  key: str | None = None,
):
  """Creates a button component, which is a composite component. Typically, you would use a text or icon component as a child.

  Intended for advanced use cases.

  Args:
    on_click: [click](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/click_event) is a native browser event.
    type: Type of button style to use
    color: Theme color palette of the button
    disable_ripple: Whether the ripple effect is disabled or not.
    disabled: Whether the button is disabled.
    style: Style for the component.
    key: The component [key](../components/index.md#component-key).
  """
  return insert_composite_component(
    key=key,
    type_name="content_button",
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
    style=style,
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
