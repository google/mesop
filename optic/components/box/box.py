from pydantic import validate_arguments

import optic.components.box.box_pb2 as box_pb
from optic.component_helpers import ComponentWithChildren


@validate_arguments
def box(
  *,
  background_color: str = "",
  key: str | None = None,
):
  """
  This function creates a box.

  Args:
      label (str): The text to be displayed
  """
  return ComponentWithChildren(
    key=key,
    type_name="box",
    proto=box_pb.BoxType(background_color=background_color),
  )
