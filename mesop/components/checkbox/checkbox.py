from dataclasses import dataclass
from typing import Any, Callable

from pydantic import validate_arguments

import mesop.components.checkbox.checkbox_pb2 as checkbox_pb
from mesop.component_helpers import (
  handler_type,
  insert_component,
  register_event_mapper,
)
from mesop.events import MesopEvent


@dataclass
class MatCheckboxChangeEvent(MesopEvent):
  checked: bool


register_event_mapper(
  MatCheckboxChangeEvent,
  lambda event, key: MatCheckboxChangeEvent(
    key=key,
    checked=event.bool,
  ),
)


@validate_arguments
def checkbox(
  *,
  key: str | None = None,
  value: bool = False,
  on_mat_checkbox_change: Callable[[MatCheckboxChangeEvent], Any] | None = None,
  label: str = "",
):
  """
  TODO_doc_string
  """
  insert_component(
    key=key,
    type_name="checkbox",
    proto=checkbox_pb.CheckboxType(
      value=value,
      on_mat_checkbox_change_handler_id=handler_type(on_mat_checkbox_change)
      if on_mat_checkbox_change
      else "",
      label=label,
    ),
  )
