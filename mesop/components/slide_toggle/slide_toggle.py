from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.slide_toggle.slide_toggle_pb2 as slide_toggle_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass
class SlideToggleChangeEvent(MesopEvent):
  """Event triggered when the slide toggle state changes.

  Attributes:
      key (str): Key of the component that emitted this event.
  """

  key: str


register_event_mapper(
  SlideToggleChangeEvent,
  lambda event, key: SlideToggleChangeEvent(
    key=key.key,
  ),
)


@register_native_component
def slide_toggle(
  *,
  key: str | None = None,
  label_position: Literal["before", "after"] = "after",
  required: bool = False,
  color: Literal["primary", "accent", "warn"] | None = None,
  disabled: bool = False,
  disable_ripple: bool = False,
  tab_index: int = 0,
  checked: bool = False,
  hide_icon: bool = False,
  on_change: Callable[[SlideToggleChangeEvent], Any] | None = None,
):
  """Creates a Slide toggle component.

  Args:
    on_change: An event will be dispatched each time the slide-toggle changes its value.
    label_position: Whether the label should appear after or before the slide-toggle. Defaults to 'after'.
    required: Whether the slide-toggle is required.
    color: Palette color of slide toggle.
    disabled: Whether the slide toggle is disabled.
    disable_ripple: Whether the slide toggle has a ripple.
    tab_index: Tabindex of slide toggle.
    checked: Whether the slide-toggle element is checked or not.
    hide_icon: Whether to hide the icon inside of the slide toggle.
    key: Unique identifier for this component instance.
  """
  return insert_composite_component(
    key=key,
    type_name="slide_toggle",
    proto=slide_toggle_pb.SlideToggleType(
      label_position=label_position,
      required=required,
      color=color,
      disabled=disabled,
      disable_ripple=disable_ripple,
      tab_index=tab_index,
      checked=checked,
      hide_icon=hide_icon,
      on_slide_toggle_change_event_handler_id=register_event_handler(
        on_change, event=SlideToggleChangeEvent
      )
      if on_change
      else "",
    ),
  )
