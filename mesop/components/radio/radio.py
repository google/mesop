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
  value: str


register_event_mapper(
  RadioChangeEvent,
  lambda event, key: RadioChangeEvent(key=key.key, value=event.string),
)


@dataclass
class RadioOption:
  """
  Members:
    id: The unique ID for the radio button.
    label: Content to show for the radio option
    aria_labelledby: The 'aria-labelledby' attribute takes precedence as the element's text alternative.
    aria_describedby: The 'aria-describedby' attribute is read after the element's label and field type.
    disable_ripple: Whether ripples are disabled inside the radio button
    tab_index: Tabindex of the radio button.
    checked: Whether this radio button is checked.
    value: The value of this radio button.
    label_position: Whether the label should appear after or before the radio button. Defaults to 'after'
    disabled: Whether the radio button is disabled.
    required: Whether the radio button is required.
    color: Theme color of the radio button.
  """

  label: str
  value: str

  id: str = ""
  aria_labelledby: str = ""
  aria_describedby: str = ""
  disable_ripple: bool = False
  tab_index: float = 0
  checked: bool = False
  label_position: Literal["before", "after"] = "before"
  disabled: bool = False
  required: bool = False
  color: Literal["primary", "accent", "warn"] = "primary"


@validate
def radio(
  options: list[RadioOption],
  *,
  key: str | None = None,
  color: Literal["primary", "accent", "warn"] = "primary",
  name: str = "",
  label_position: Literal["before", "after"] = "before",
  value: str = "",
  disabled: bool = False,
  required: bool = False,
  on_change: Callable[[RadioChangeEvent], Any] | None = None,
):
  """Creates a Radio component.

  Args:
    key: Unique identifier for this component instance.
    radio_options: List of radio options
    color: Theme color for all of the radio buttons in the group.
    label_position: Whether the labels should appear after or before the radio-buttons. Defaults to 'after'
    value: Value for the radio-group. Should equal the value of the selected radio button if there is a corresponding radio button with a matching value. If there is not such a corresponding radio button, this value persists to be applied in case a new radio button is added with a matching value.
    disabled: Whether the radio group is disabled
    required: Whether the radio group is required

    on_change: Event emitted when the group value changes. Change events are only emitted when the value changes due to user interaction with a radio button (the same behavior as `<input type-"radio">`).
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
          id=option.id,
          label=option.label,
          aria_labelledby=option.aria_labelledby,
          aria_describedby=option.aria_describedby,
          disable_ripple=option.disable_ripple,
          tab_index=option.tab_index,
          checked=option.checked,
          value=option.value,
          label_position=option.label_position,
          disabled=option.disabled,
          required=option.required,
          color=option.color,
        )
        for option in options
      ],
    ),
  )
