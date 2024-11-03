from dataclasses import dataclass
from typing import Any, Callable

import mesop.components.expansion_panel.expansion_panel_pb2 as expansion_panel_pb
from mesop.component_helpers import (
  Style,
  insert_composite_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class ExpansionPanelToggleEvent(MesopEvent):
  """Event representing the opening/closing of the expansion panel.

  Attributes:
      opened: Whether the expansion panel is opened.
      key (str): key of the component that emitted this event.
  """

  opened: bool


register_event_mapper(
  ExpansionPanelToggleEvent,
  lambda event, key: ExpansionPanelToggleEvent(
    key=key.key, opened=event.bool_value
  ),
)


@register_native_component
def expansion_panel(
  *,
  title: str,
  description: str = "",
  icon: str = "",
  disabled: bool = False,
  expanded: bool | None = None,
  hide_toggle: bool = False,
  on_toggle: Callable[[ExpansionPanelToggleEvent], Any] | None = None,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates an expansion_panel.

  Args:
      title: Title of the panel.
      description: Optional brief description of the panel.
      icon: Optional icon from https://fonts.google.com/icons.
      disabled: Whether the panel is disabled.
      expanded: Whether the toggle is expanded. Use `None` if you do not need to manage open/closed state.
      hide_toggle: Whether to the toggle is shown.
      on_toggle: Event fired when the expansion panel header is opened/closed.
      style: Style for the component.
      key: The component [key](../components/index.md#component-key).
  """
  return insert_composite_component(
    key=key,
    type_name="expansion_panel",
    style=style,
    proto=expansion_panel_pb.ExpansionPanelType(
      title=title,
      description=description,
      icon=icon,
      disabled=disabled,
      expanded=str(expanded),
      hide_toggle=hide_toggle,
      on_toggle_handler_id=register_event_handler(
        on_toggle, event=ExpansionPanelToggleEvent
      )
      if on_toggle
      else "",
    ),
  )
