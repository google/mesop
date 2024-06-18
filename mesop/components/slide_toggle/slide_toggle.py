from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.slide_toggle.slide_toggle_pb2 as slide_toggle_pb
from mesop.component_helpers import (
  component,
  insert_composite_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.components.text.text import text
from mesop.events import MesopEvent


@dataclass(kw_only=True)
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


@component()
def slide_toggle(
  label: str | None = None,
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
  """Creates a simple Slide toggle component with a text label.

  Args:
    label: Text label for slide toggle
    on_change: An event will be dispatched each time the slide-toggle changes its value.
    label_position: Whether the label should appear after or before the slide-toggle. Defaults to 'after'.
    required: Whether the slide-toggle is required.
    color: Palette color of slide toggle.
    disabled: Whether the slide toggle is disabled.
    disable_ripple: Whether the slide toggle has a ripple.
    tab_index: Tabindex of slide toggle.
    checked: Whether the slide-toggle element is checked or not.
    hide_icon: Whether to hide the icon inside of the slide toggle.
    key: The component [key](../components/index.md#component-key).
  """
  with content_slide_toggle(
    key=key,
    label_position=label_position,
    required=required,
    color=color,
    disabled=disabled,
    disable_ripple=disable_ripple,
    tab_index=tab_index,
    checked=checked,
    hide_icon=hide_icon,
    on_change=on_change,
  ):
    text(label)


@register_native_component
def content_slide_toggle(
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
  """Creates a Slide toggle component which is a composite component. Typically, you would use a text or icon component as a child.

  Intended for advanced use cases.


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
    key: The component [key](../components/index.md#component-key).
  """
  return insert_composite_component(
    key=key,
    type_name="content_slide_toggle",
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
