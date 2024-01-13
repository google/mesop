from dataclasses import dataclass
from typing import Any, Callable, Iterable

import mesop.components.select.select_pb2 as select_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass
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


@dataclass
class SelectSelectionChangeEvent(MesopEvent):
  """Event representing a change in the select component's value.

  Attributes:
      value: The new value of the select component after the change.
      key (str): Key of the component that emitted this event.
  """

  value: str


register_event_mapper(
  SelectSelectionChangeEvent,
  lambda event, key: SelectSelectionChangeEvent(
    key=key.key,
    value=event.string_value,
  ),
)


@dataclass
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
):
  """Creates a Select component.

  Args:
    options: List of select options.
    on_selection_change: Event emitted when the selected value has been changed by the user.
    on_opened_change: Event emitted when the select panel has been toggled.
    disabled: Whether the select is disabled.
    disable_ripple: Whether ripples in the select are disabled.
    tab_index: Tab index of the select.
    placeholder: Placeholder to be shown if no value has been selected.
    value: Value of the select control.
    key: Unique identifier for this component instance.
  """
  insert_component(
    key=key,
    type_name="select",
    proto=select_pb.SelectType(
      options=[
        select_pb.SelectOption(label=option.label, value=option.value)
        for option in options
      ],
      label=label,
      disabled=disabled,
      disable_ripple=disable_ripple,
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
