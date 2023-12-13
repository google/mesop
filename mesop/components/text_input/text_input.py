from typing import Any, Callable

from pydantic import validate_arguments

import mesop.components.text_input.text_input_pb2 as text_input_pb
from mesop.component_helpers import handler_type, insert_component
from mesop.events import ChangeEvent


@validate_arguments
def text_input(
  *,
  label: str,
  on_change: Callable[[ChangeEvent], Any],
  key: str | None = None,
):
  """
  Creates a text input.

  Args:
      label (str): The text to be displayed
      on_change (Callable[..., Any]): Called when user changes text input value.
  """
  insert_component(
    key=key,
    type_name="text_input",
    proto=text_input_pb.TextInputType(
      label=label,
      on_change_handler_id=handler_type(on_change),
    ),
  )
