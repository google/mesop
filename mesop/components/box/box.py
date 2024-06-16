from typing import Any, Callable

import mesop.components.box.box_pb2 as box_pb
from mesop.component_helpers import (
  Style,
  insert_composite_component,
  register_event_handler,
  register_native_component,
)
from mesop.events import ClickEvent


@register_native_component
def box(
  *,
  style: Style | None = None,
  on_click: Callable[[ClickEvent], Any] | None = None,
  key: str | None = None,
) -> Any:
  """Creates a box component.

  Args:
    style: Style to apply to component. Follows [HTML Element inline style API](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style).
    on_click: The callback function that is called when the box is clicked.
      It receives a ClickEvent as its only argument.
    key: The component [key](../components/index.md#component-key).

  Returns:
    The created box component.
  """
  return insert_composite_component(
    key=key,
    type_name="box",
    proto=box_pb.BoxType(
      on_click_handler_id=register_event_handler(on_click, event=ClickEvent)
      if on_click
      else "",
    ),
    style=style,
  )
