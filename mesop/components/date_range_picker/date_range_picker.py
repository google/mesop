from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Callable, Literal

import mesop.components.date_range_picker.date_range_picker_pb2 as date_range_picker_pb
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
class DateRangePickerChangeEvent(MesopEvent):
  """Represents a date range picker change event.

  This event will only fire if start and end dates are valid dates.

  Attributes:
      start_date: Start date
      end_date: End date
      key (str): key of the component that emitted this event.
  """

  start_date: date
  end_date: date


register_event_mapper(
  DateRangePickerChangeEvent,
  lambda userEvent, key: DateRangePickerChangeEvent(
    start_date=_try_make_date(userEvent.date_range_picker_event.start_date),
    end_date=_try_make_date(userEvent.date_range_picker_event.end_date),
    key=key.key,
  ),
)


@register_native_component
def date_range_picker(
  *,
  label: str = "",
  on_change: Callable[[DateRangePickerChangeEvent], Any] | None = None,
  appearance: Literal["fill", "outline"] = "fill",
  style: Style | None = None,
  disabled: bool = False,
  placeholder_start_date: str = "",
  placeholder_end_date: str = "",
  required: bool = False,
  start_date: date | None = None,
  end_date: date | None = None,
  readonly: bool = False,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "auto",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
  key: str | None = None,
):
  """Creates a date range picker component.

  Args:
    label: Label for date range picker input.
    on_change: Fires when valid date values for both start/end have been specified through Calendar date selection or user input blur.
    appearance: The form field appearance style.
    style: Style for date range picker input.
    disabled: Whether it's disabled.
    placeholder_start_date: Start date placeholder value.
    placeholder_end_date: End date placeholder value.
    required: Whether it's required.
    start_date: Start date initial value.
    end_date: End date initial value.
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
    type_name="date_range_picker",
    proto=date_range_picker_pb.DateRangePickerType(
      start_date=_try_make_date_str(start_date),
      end_date=_try_make_date_str(end_date),
      placeholder_start_date=placeholder_start_date,
      placeholder_end_date=placeholder_end_date,
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
        on_change, event=DateRangePickerChangeEvent
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
