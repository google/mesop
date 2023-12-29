from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.checkbox.checkbox_pb2 as checkbox_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_event_handler,
  register_event_mapper,
)
from mesop.events import MesopEvent
from mesop.utils.validate import validate


@dataclass
class CheckboxChangeEvent(MesopEvent):
  """Represents a checkbox state change event.

  Attributes:
      checked: The new checked state of the checkbox.
      key (str): key of the component that emitted this event.
  """

  checked: bool


register_event_mapper(
  CheckboxChangeEvent,
  lambda event, key: CheckboxChangeEvent(
    key=key.key,
    checked=event.bool_value,
  ),
)


@dataclass
class CheckboxIndeterminateChangeEvent(MesopEvent):
  """Represents a checkbox indeterminate state change event.

  Attributes:
      checked: The new indeterminate state of the checkbox.
      key (str): key of the component that emitted this event.
  """

  indeterminate: bool


register_event_mapper(
  CheckboxIndeterminateChangeEvent,
  lambda event, key: CheckboxIndeterminateChangeEvent(
    key=key.key,
    indeterminate=event.bool_value,
  ),
)


@validate
def checkbox(
  *,
  on_change: Callable[[CheckboxChangeEvent], Any] | None = None,
  on_indeterminate_change: Callable[[CheckboxIndeterminateChangeEvent], Any]
  | None = None,
  required: bool = False,
  label_position: Literal["before", "after"] = "after",
  name: str = "",
  value: str = "",
  disable_ripple: bool = False,
  tab_index: float = 0,
  color: str = "",
  checked: bool = False,
  disabled: bool = False,
  indeterminate: bool = False,
  key: str | None = None,
):
  """Creates a Checkbox component.
  Checkbox is a composite component.

  Args:
    on_change: Event emitted when the checkbox's `checked` value changes.
    on_indeterminate_change: Event emitted when the checkbox's `indeterminate` value changes.
    required: Whether the checkbox is required.
    label_position: Whether the label should appear after or before the checkbox. Defaults to 'after'
    name: Name value will be applied to the input element if present
    value: The value attribute of the native input element
    disable_ripple: Whether the checkbox has a ripple.
    tab_index: Tabindex for the checkbox.
    color: Palette color of the checkbox.
    checked: Whether the checkbox is checked.
    disabled: Whether the checkbox is disabled.
    indeterminate: Whether the checkbox is indeterminate. This is also known as "mixed" mode and can be used to represent a checkbox with three states, e.g. a checkbox that represents a nested list of checkable items. Note that whenever checkbox is manually clicked, indeterminate is immediately set to false.
    key: Unique identifier for this component instance.
  """
  return insert_composite_component(
    key=key,
    type_name="checkbox",
    proto=checkbox_pb.CheckboxType(
      required=required,
      label_position=label_position,
      name=name,
      value=value,
      disable_ripple=disable_ripple,
      tab_index=tab_index,
      color=color,
      checked=checked,
      disabled=disabled,
      indeterminate=indeterminate,
      on_checkbox_change_event_handler_id=register_event_handler(
        on_change, event=CheckboxChangeEvent
      )
      if on_change
      else "",
      on_checkbox_indeterminate_change_event_handler_id=register_event_handler(
        on_indeterminate_change, event=CheckboxIndeterminateChangeEvent
      )
      if on_indeterminate_change
      else "",
    ),
  )
