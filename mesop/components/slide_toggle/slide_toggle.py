from dataclasses import dataclass
from typing import Any, Callable, Literal

from pydantic import validate_arguments

import mesop.components.slide_toggle.slide_toggle_pb2 as slide_toggle_pb
from mesop.component_helpers import (
  handler_type,
  insert_component,
  register_event_mapper,
)
from mesop.events import MesopEvent


@dataclass
class SlideToggleChangeEvent(MesopEvent):
  pass


register_event_mapper(
  SlideToggleChangeEvent,
  lambda event, key: SlideToggleChangeEvent(
    key=key,
  ),
)


@validate_arguments
def slide_toggle(
  *,
  key: str | None = None,
  name: str = "",
  id: str = "",
  label_position: Literal["before", "after"] = "after",
  aria_label: str = "",
  aria_labelledby: str = "",
  aria_describedby: str = "",
  required: bool = False,
  color: str = "",
  disabled: bool = False,
  disable_ripple: bool = False,
  tab_index: float = 0,
  checked: bool = False,
  hide_icon: bool = False,
  on_change: Callable[[SlideToggleChangeEvent], Any] | None = None,
):
  """Creates a Slide toggle component.

  Args:
    key (str|None): Unique identifier for this component instance.
    name (str): Name value will be applied to the input element if present.
    id (str): A unique id for the slide-toggle input. If none is supplied, it will be auto-generated.
    label_position (Literal['before','after']): Whether the label should appear after or before the slide-toggle. Defaults to 'after'.
    aria_label (str): Used to set the aria-label attribute on the underlying input element.
    aria_labelledby (str): Used to set the aria-labelledby attribute on the underlying input element.
    aria_describedby (str): Used to set the aria-describedby attribute on the underlying input element.
    required (bool): Whether the slide-toggle is required.
    color (str): Palette color of slide toggle.
    disabled (bool): Whether the slide toggle is disabled.
    disable_ripple (bool): Whether the slide toggle has a ripple.
    tab_index (float): Tabindex of slide toggle.
    checked (bool): Whether the slide-toggle element is checked or not.
    hide_icon (bool): Whether to hide the icon inside of the slide toggle.
    on_change (Callable[[SlideToggleChangeEvent], Any]|None): An event will be dispatched each time the slide-toggle changes its value.
  """
  insert_component(
    key=key,
    type_name="slide_toggle",
    proto=slide_toggle_pb.SlideToggleType(
      name=name,
      id=id,
      label_position=label_position,
      aria_label=aria_label,
      aria_labelledby=aria_labelledby,
      aria_describedby=aria_describedby,
      required=required,
      color=color,
      disabled=disabled,
      disable_ripple=disable_ripple,
      tab_index=tab_index,
      checked=checked,
      hide_icon=hide_icon,
      on_slide_toggle_change_event_handler_id=handler_type(on_change)
      if on_change
      else "",
    ),
  )
