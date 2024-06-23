from dataclasses import dataclass
from typing import Any, Callable, Iterable, Literal

import mesop.components.radio.radio_pb2 as radio_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
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


@dataclass(kw_only=True)
class RadioOption:
  """
  Attributes:
    label: Content to show for the radio option
    value: The value of this radio button.
  """

  label: str | None = None
  value: str | None = None


@register_native_component
def radio(
  *,
  options: Iterable[RadioOption] = (),
  on_change: Callable[[RadioChangeEvent], Any] | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  label_position: Literal["before", "after"] = "after",
  value: str = "",
  disabled: bool = False,
  style: Style | None = None,
  key: str | None = None,
):
  """Creates a Radio component.

  Args:
    options: List of radio options
    on_change: Event emitted when the group value changes. Change events are only emitted when the value changes due to user interaction with a radio button (the same behavior as `<input type-"radio">`).
    color: Theme color for all of the radio buttons in the group.
    label_position: Whether the labels should appear after or before the radio-buttons. Defaults to 'after'
    value: Value for the radio-group. Should equal the value of the selected radio button if there is a corresponding radio button with a matching value.
    disabled: Whether the radio group is disabled.
    style: Style for the component.
    key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="radio",
    proto=radio_pb.RadioType(
      color=color,
      label_position=label_position,
      value=value,
      disabled=disabled,
      on_radio_change_event_handler_id=register_event_handler(
        on_change, event=RadioChangeEvent
      )
      if on_change
      else "",
      options=[
        radio_pb.RadioOption(
          label=option.label,
          value=option.value,
        )
        for option in options
      ],
    ),
    style=style,
  )
