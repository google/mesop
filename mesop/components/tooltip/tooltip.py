from typing import Literal

import mesop.components.tooltip.tooltip_pb2 as tooltip_pb
from mesop.component_helpers import (
  insert_composite_component,
)
from mesop.utils.validate import validate


@validate
def tooltip(
  *,
  key: str | None = None,
  position: Literal[
    "left", "right", "above", "below", "before", "after"
  ] = "left",
  position_at_origin: bool = False,
  disabled: bool = False,
  show_delay: float = 0,
  hide_delay: float = 0,
  touch_gestures: Literal["auto", "on", "off"] = "auto",
  message: str = "",
):
  """Creates a Tooltip component.
  Tooltip is a composite component.

  Args:
    key: Unique identifier for this component instance.
    position: Allows the user to define the position of the tooltip relative to the parent element
    position_at_origin: Whether tooltip should be relative to the click or touch origin instead of outside the element bounding box.
    disabled: Disables the display of the tooltip.
    show_delay: The default delay in ms before showing the tooltip after show is called
    hide_delay: The default delay in ms before hiding the tooltip after hide is called
    touch_gestures: How touch gestures should be handled by the tooltip. On touch devices the tooltip directive uses a long press gesture to show and hide, however it can conflict with the native browser gestures. To work around the conflict, Angular Material disables native gestures on the trigger, but that might not be desirable on particular elements (e.g. inputs and draggable elements). The different values for this option configure the touch event handling as follows: - `auto` - Enables touch gestures for all elements, but tries to avoid conflicts with native   browser gestures on particular elements. In particular, it allows text selection on inputs   and textareas, and preserves the native browser dragging on elements marked as `draggable`. - `on` - Enables touch gestures for all elements and disables native   browser gestures with no exceptions. - `off` - Disables touch gestures. Note that this will prevent the tooltip from   showing on touch devices.
    message: The message to be displayed in the tooltip
  """
  return insert_composite_component(
    key=key,
    type_name="tooltip",
    proto=tooltip_pb.TooltipType(
      position=position,
      position_at_origin=position_at_origin,
      disabled=disabled,
      show_delay=show_delay,
      hide_delay=hide_delay,
      touch_gestures=touch_gestures,
      message=message,
    ),
  )
