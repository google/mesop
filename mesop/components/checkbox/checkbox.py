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
class CheckboxEvent(MesopEvent):
  checked: bool


@validate_arguments
def checkbox(
  *,
  label: str,
  on_update: Callable[[CheckboxEvent], Any],
  default_value: bool = False,
  key: str | None = None,
):
  """
  Creates a checkbox component with a specified label and update action.

  Args:
      label (str): The label for the checkbox.
      on_update (Callable[..., Any]): The function to be called when the checkbox is updated.

  The function appends the created checkbox component to the children of the current node in the runtime context.
  """
  insert_component(
    key=key,
    type_name="checkbox",
    proto=checkbox_pb.CheckboxType(
      label=label,
      on_update_handler_id=handler_type(on_update),
      default_value=default_value,
    ),
  )


register_event_mapper(
  CheckboxEvent,
  lambda userEvent, key: CheckboxEvent(
    key=key,
    checked=userEvent.bool,
  ),
)
