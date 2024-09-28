from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Callable, Literal

import mesop.components.datepicker.datepicker_pb2 as datepicker_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent

_DATE_FORMAT = "%Y-%m-%d"


@dataclass(kw_only=True)
class DatePickerChangeEvent(MesopEvent):
  """Represents a date picker change event.

  This event will only fire if a valid date is specified.

  Attributes:
      date: Date value
      key (str): key of the component that emitted this event.
  """

  date: date


register_event_mapper(
  DatePickerChangeEvent,
  lambda userEvent, key: DatePickerChangeEvent(
    date=_try_make_date(userEvent.string_value),
    key=key.key,
  ),
)


@register_native_component
def date_picker(
  *,
  label: str = "",
  on_change: Callable[[DatePickerChangeEvent], Any] | None = None,
  appearance: Literal["fill", "outline"] = "fill",
  style: Style | None = None,
  disabled: bool = False,
  placeholder: str = "",
  required: bool = False,
  value: date | None = None,
  readonly: bool = False,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "auto",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
  key: str | None = None,
):
  """Creates a date picker component.

  Args:
    label: Label for date picker input.
    on_change: Fires when a valid date value has been specified through Calendar date selection or user input blur.
    appearance: The form field appearance style.
    style: Style for date picker input.
    disabled: Whether it's disabled.
    placeholder: Placeholder value.
    required: Whether it's required.
    value: Initial value.
    readonly: Whether the element is readonly.
    hide_required_marker: Whether the required marker should be hidden.
    color: The color palette for the form field.
    float_label: Whether the label should always float or float as the user types.
    subscript_sizing: Whether the form field should reserve space for one line of hint/error text (default) or to have the spacing grow from 0px as needed based on the size of the hint/error content. Note that when using dynamic sizing, layout shifts will occur when hint/error text changes.
    hint_label: Text for the form field hint.
    key: The component [key](../components/index.md#component-key).
  """

  insert_component(
    key=key,
    type_name="datepicker",
    proto=datepicker_pb.DatePickerType(
      value=_try_make_date_str(value),
      placeholder=placeholder,
      disabled=disabled,
      required=required,
      readonly=readonly,
      hide_required_marker=hide_required_marker,
      color=color,
      float_label=float_label,
      appearance=appearance,
      subscript_sizing=subscript_sizing,
      hint_label=hint_label,
      label=label,
      on_change_handler_id=register_event_handler(
        on_change, event=DatePickerChangeEvent
      )
      if on_change
      else "",
    ),
    style=style,
  )


def _try_make_date_str(date_input: date | None) -> str:
  if date_input:
    return date_input.isoformat()
  return ""


def _try_make_date(date_string: str) -> date:
  return datetime.strptime(date_string, _DATE_FORMAT).date()
