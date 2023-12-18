from typing import Literal

from pydantic import validate_arguments

import mesop.components.progress_spinner.progress_spinner_pb2 as progress_spinner_pb
from mesop.component_helpers import (
  insert_component,
)


@validate_arguments
def progress_spinner(
  *,
  key: str | None = None,
  color: str = "",
  mode: Literal["determinate", "indeterminate"] = "determinate",
  value: float = 0,
  diameter: float = 0,
  stroke_width: float = 0,
):
  """Creates a Progress spinner component.

  Args:
    key: Unique identifier for this component instance.
    color: Theme palette color of the progress spinner.
    mode: Mode of the progress bar. Input must be one of these values: determinate, indeterminate, buffer, query, defaults to 'determinate'. Mirrored to mode attribute.
    value: Value of the progress bar. Defaults to zero. Mirrored to aria-valuenow.
    diameter: The diameter of the progress spinner (will set width and height of svg).
    stroke_width: Stroke width of the progress spinner.
  """
  insert_component(
    key=key,
    type_name="progress_spinner",
    proto=progress_spinner_pb.ProgressSpinnerType(
      color=color,
      mode=mode,
      value=value,
      diameter=diameter,
      stroke_width=stroke_width,
    ),
  )
