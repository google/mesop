from dataclasses import dataclass
from typing import Any, Callable, Iterable

import mesop.components.select.select_pb2 as select_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class SelectOpenedChangeEvent(MesopEvent):
  """Event representing the opened state change of the select component.

  Attributes:
      opened: A boolean indicating whether the select component is opened (True) or closed (False).
      key (str): key of the component that emitted this event.
  """

  opened: bool


register_event_mapper(
  SelectOpenedChangeEvent,
  lambda event, key: SelectOpenedChangeEvent(
    key=key.key,
    opened=event.bool_value,
  ),
)


@dataclass(kw_only=True)
class SelectSelectionChangeEvent(MesopEvent):
  """Event representing a change in the select component's value(s).

  Attributes:
      values: New values of the select component after the change.
      key (str): Key of the component that emitted this event.
  """

  values: list[str]

  @property
  def value(self):
    """Shortcut for returning a single value."""
    if not self.values:
      return ""
    return self.values[0]


def map_select_change_event(event, key):
  select_event = select_pb.SelectChangeEvent()
  select_event.ParseFromString(event.bytes_value)
  return SelectSelectionChangeEvent(
    key=key.key,
    values=list(select_event.values),
  )


register_event_mapper(SelectSelectionChangeEvent, map_select_change_event)


@dataclass(kw_only=True)
class SelectOption:
  """Represents an option within a select component.

  Attributes:
      label: The content shown for the select option.
      value: The value associated with the select option.
  """

  label: str | None = None
  value: str | None = None


@register_native_component
def select(
  *,
  options: Iterable[SelectOption] = (),
  on_selection_change: Callable[[SelectSelectionChangeEvent], Any]
  | None = None,
  on_opened_change: Callable[[SelectOpenedChangeEvent], Any] | None = None,
  key: str | None = None,
  label: str = "",
  disabled: bool = False,
  disable_ripple: bool = False,
  tab_index: int = 0,
  placeholder: str = "",
  value: str = "",
  style: Style | None = None,
  multiple: bool = False,
):
  """Creates a Select component.

  Args:
    options: List of select options.
    on_selection_change: Event emitted when the selected value has been changed by the user.
    on_opened_change: Event emitted when the select panel has been toggled.
    disabled: Whether the select is disabled.
    disable_ripple: Whether ripples in the select are disabled.
    multiple: Whether multiple selections are allowed.
    tab_index: Tab index of the select.
    placeholder: Placeholder to be shown if no value has been selected.
    value: Value of the select control.
    style: Style.
    key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="select",
    style=style,
    proto=select_pb.SelectType(
      options=[
        select_pb.SelectOption(label=option.label, value=option.value)
        for option in options
      ],
      label=label,
      disabled=disabled,
      disable_ripple=disable_ripple,
      multiple=multiple,
      tab_index=tab_index,
      placeholder=placeholder,
      value=value,
      on_select_opened_change_event_handler_id=register_event_handler(
        on_opened_change, event=SelectOpenedChangeEvent
      )
      if on_opened_change
      else "",
      on_select_selection_change_event_handler_id=register_event_handler(
        on_selection_change, event=SelectSelectionChangeEvent
      )
      if on_selection_change
      else "",
    ),
  )
