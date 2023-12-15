from dataclasses import dataclass
from typing import Any, Callable, Literal

from pydantic import validate_arguments

import mesop.components.checkbox.checkbox_pb2 as checkbox_pb
from mesop.component_helpers import (
  handler_type,
  insert_composite_component,
  register_event_mapper,
)
from mesop.events import MesopEvent


@dataclass
class CheckboxChangeEvent(MesopEvent):
  checked: bool


register_event_mapper(
  CheckboxChangeEvent,
  lambda event, key: CheckboxChangeEvent(
    key=key,
    checked=event.bool,
  ),
)


@dataclass
class CheckboxIndeterminateChangeEvent(MesopEvent):
  indeterminate: bool


register_event_mapper(
  CheckboxIndeterminateChangeEvent,
  lambda event, key: CheckboxIndeterminateChangeEvent(
    key=key,
    indeterminate=event.bool,
  ),
)


@validate_arguments
def checkbox(
  *,
  key: str | None = None,
  aria_label: str = "",
  aria_labelledby: str = "",
  aria_describedby: str = "",
  id: str = "",
  required: bool = False,
  label_position: Literal["before", "after"] | None = None,
  name: str = "",
  value: str = "",
  disable_ripple: bool = False,
  tab_index: float = 0,
  color: str = "",
  on_change: Callable[[CheckboxChangeEvent], Any] | None = None,
  on_indeterminate_change: Callable[[CheckboxIndeterminateChangeEvent], Any]
  | None = None,
):
  """
  TODO_doc_string
  """
  return insert_composite_component(
    key=key,
    type_name="checkbox",
    proto=checkbox_pb.CheckboxType(
      aria_label=aria_label,
      aria_labelledby=aria_labelledby,
      aria_describedby=aria_describedby,
      id=id,
      required=required,
      label_position=label_position,
      name=name,
      value=value,
      disable_ripple=disable_ripple,
      tab_index=tab_index,
      color=color,
      on_checkbox_change_event_handler_id=handler_type(on_change)
      if on_change
      else "",
      on_checkbox_indeterminate_change_event_handler_id=handler_type(
        on_indeterminate_change
      )
      if on_indeterminate_change
      else "",
    ),
  )
