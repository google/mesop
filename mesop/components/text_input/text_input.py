from typing import Any, Callable

from pydantic import validate_arguments

import mesop.components.text_input.text_input_pb2 as text_input_pb
from mesop.component_helpers import insert_component, register_event_handler
from mesop.events import ChangeEvent


@validate_arguments
def text_input(
  *,
  label: str,
  on_change: Callable[[ChangeEvent], Any],
  default_value: str = "",
  key: str | None = None,
):
  """
  Creates a text input.

  Args:
      label: The text to be displayed
      on_change: Called when user changes text input value.
  """
  insert_component(
    key=key,
    type_name="text_input",
    proto=text_input_pb.TextInputType(
      label=label,
      default_value=default_value,
      on_change_handler_id=register_event_handler(on_change, event=ChangeEvent),
    ),
  )
