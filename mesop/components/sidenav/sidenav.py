from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.sidenav.sidenav_pb2 as sidenav_pb
from mesop.component_helpers import (
  Style,
  insert_composite_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class SidenavOpenedChangedEvent(MesopEvent):
  """Event representing the opened state change of the sidenav component.

  Attributes:
      opened: A boolean indicating whether the sidenav component is opened (True) or closed (False).
      key (str): key of the component that emitted this event.
  """

  opened: bool


register_event_mapper(
  SidenavOpenedChangedEvent,
  lambda event, key: SidenavOpenedChangedEvent(
    key=key.key,
    opened=event.bool_value,
  ),
)


@register_native_component
def sidenav(
  *,
  opened: bool = True,
  disable_close: bool = True,
  position: Literal["start", "end"] = "start",
  on_opened_changed: Callable[[SidenavOpenedChangedEvent], Any] | None = None,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a sidenav.

  Args:
      opened: A flag to determine if the sidenav is open or closed. Defaults to True.
      disable_close: Whether the drawer can be closed with the escape key.
      position: The side that the drawer is attached to.
      on_opened_changed: Handles event emitted when the drawer open state is changed.
      style: An optional Style object to apply custom styles. Defaults to None.
      key: The component [key](../components/index.md#component-key).
  """
  return insert_composite_component(
    key=key,
    type_name="sidenav",
    style=style,
    proto=sidenav_pb.SidenavType(
      opened=opened,
      disable_close=disable_close,
      position=position,
      on_opened_changed_event_handler_id=register_event_handler(
        on_opened_changed, event=SidenavOpenedChangedEvent
      )
      if on_opened_changed
      else "",
    ),
  )
