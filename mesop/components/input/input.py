from pydantic import validate_arguments

import mesop.components.input.input_pb2 as input_pb
from mesop.component_helpers import insert_component


@validate_arguments
def input(
  *,
  label: str,
  key: str | None = None,
):
  """
  This function creates a input.

  Args:
      label (str): The text to be displayed
  """
  insert_component(
    key=key,
    type_name="input",
    proto=input_pb.InputType(
      label=label,
    ),
  )
