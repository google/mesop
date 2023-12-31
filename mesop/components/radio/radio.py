from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.radio.radio_pb2 as radio_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
)
from mesop.events import MesopEvent
from mesop.utils.validate import validate


@dataclass
class RadioChangeEvent(MesopEvent):
  """Event representing a change in the radio component's value.

  Attributes:
      value: The new value of the radio component after the change.
      key (str): key of the component that emitted this event.
  """

  value: str


register_event_mapper(
  RadioChangeEvent,
  lambda event, key: RadioChangeEvent(key=key.key, value=event.string_value),
)


@dataclass
class RadioOption:
  """
  Attributes:
    label: Content to show for the radio option
    value: The value of this radio button.
  """

  label: str
  value: str


@validate
def radio(
  options: list[RadioOption],
  *,
  on_change: Callable[[RadioChangeEvent], Any] | None = None,
  color: Literal["primary", "accent", "warn"] = "primary",
  label_position: Literal["before", "after"] = "before",
  value: str = "",
  disabled: bool = False,
  required: bool = False,
  key: str | None = None,
):
  """Creates a Radio component.

  Args:
    options: List of radio options
    on_change: Event emitted when the group value changes. Change events are only emitted when the value changes due to user interaction with a radio button (the same behavior as `<input type-"radio">`).
    color: Theme color for all of the radio buttons in the group.
    label_position: Whether the labels should appear after or before the radio-buttons. Defaults to 'after'
    value: Value for the radio-group. Should equal the value of the selected radio button if there is a corresponding radio button with a matching value.
    disabled: Whether the radio group is disabled
    required: Whether the radio group is required
    key: Unique identifier for this component instance.
  """
  insert_component(
    key=key,
    type_name="radio",
    proto=radio_pb.RadioType(
      color=color,
      label_position=label_position,
      value=value,
      disabled=disabled,
      required=required,
      on_radio_change_event_handler_id=register_event_handler(
        on_change, event=RadioChangeEvent
      )
      if on_change
      else "",
      radio_options=[
        radio_pb.RadioOption(
          label=option.label,
          value=option.value,
        )
        for option in options
      ],
    ),
  )
