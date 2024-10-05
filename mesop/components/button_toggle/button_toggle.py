from dataclasses import dataclass
from typing import Any, Callable, Iterable

import mesop.components.button_toggle.button_toggle_pb2 as button_toggle_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class ButtonToggleChangeEvent(MesopEvent):
  """Event representing a change in the button toggle component's selected values.

  Attributes:
      values: The new values of the button toggle component after the change.
      key (str): key of the component that emitted this event.
  """

  values: list[str]

  @property
  def value(self):
    """Shortcut for returning a single value."""
    if not self.values:
      return ""
    return self.values[0]


def map_change_event(event, key):
  change_event = button_toggle_pb.ButtonToggleChangeEvent()
  change_event.ParseFromString(event.bytes_value)
  return ButtonToggleChangeEvent(
    key=key.key,
    values=list(change_event.values),
  )


register_event_mapper(ButtonToggleChangeEvent, map_change_event)


@dataclass(kw_only=True)
class ButtonToggleButton:
  """
  Attributes:
    label: Content to show for the button toggle button
    value: The value of the button toggle button.
  """

  label: str | None = None
  value: str | None = None


@register_native_component
def button_toggle(
  *,
  value: list[str] | str = "",
  buttons: Iterable[ButtonToggleButton],
  on_change: Callable[[ButtonToggleChangeEvent], Any] | None = None,
  multiple: bool = False,
  disabled: bool = False,
  hide_selection_indicator: bool = False,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a button toggle.

  Args:
    value: Selected values of the button toggle.
    buttons: List of button toggles.
    on_change: Event emitted when the group's value changes.
    multiple: Whether multiple button toggles can be selected.
    disabled: Whether multiple button toggle group is disabled.
    hide_selection_indicator: Whether checkmark indicator for button toggle groups is hidden.
    style: Style for the component.
    key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="button_toggle",
    proto=button_toggle_pb.ButtonToggleType(
      value=_format_value_field_proto(value),
      buttons=[
        button_toggle_pb.ButtonToggleButton(
          label=button.label,
          value=button.value,
        )
        for button in buttons
      ],
      multiple=multiple,
      disabled=disabled,
      hide_selection_indicator=hide_selection_indicator,
      on_change_event_handler_id=register_event_handler(
        on_change, event=ButtonToggleChangeEvent
      )
      if on_change
      else "",
    ),
    style=style,
  )


def _format_value_field_proto(value: list[str] | str):
  if not value:
    return []

  if isinstance(value, list):
    return value

  return [value]
