from typing import Literal

import mesop.components.tooltip.tooltip_pb2 as tooltip_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_native_component,
)


@register_native_component
def tooltip(
  *,
  key: str | None = None,
  position: Literal[
    "left", "right", "above", "below", "before", "after"
  ] = "left",
  position_at_origin: bool = False,
  disabled: bool = False,
  show_delay_ms: int = 0,
  hide_delay_ms: int = 0,
  message: str = "",
):
  """Creates a Tooltip component.
  Tooltip is a composite component.

  Args:
    key: The component [key](../components/index.md#component-key).
    position: Allows the user to define the position of the tooltip relative to the parent element
    position_at_origin: Whether tooltip should be relative to the click or touch origin instead of outside the element bounding box.
    disabled: Disables the display of the tooltip.
    show_delay_ms: The default delay in ms before showing the tooltip after show is called
    hide_delay_ms: The default delay in ms before hiding the tooltip after hide is called
    message: The message to be displayed in the tooltip
  """
  return insert_composite_component(
    key=key,
    type_name="tooltip",
    proto=tooltip_pb.TooltipType(
      position=position,
      position_at_origin=position_at_origin,
      disabled=disabled,
      show_delay_ms=show_delay_ms,
      hide_delay_ms=hide_delay_ms,
      message=message,
    ),
  )
