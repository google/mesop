from typing import Literal

import mesop.components.progress_spinner.progress_spinner_pb2 as progress_spinner_pb
from mesop.component_helpers import (
  insert_component,
  register_native_component,
)


@register_native_component
def progress_spinner(
  *,
  key: str | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  diameter: float = 48,
  stroke_width: float = 4,
):
  """Creates a Progress spinner component.

  Args:
    key: The component [key](../components/index.md#component-key).
    color: Theme palette color of the progress spinner.
    diameter: The diameter of the progress spinner (will set width and height of svg).
    stroke_width: Stroke width of the progress spinner.
  """
  insert_component(
    key=key,
    type_name="progress_spinner",
    proto=progress_spinner_pb.ProgressSpinnerType(
      color=color,
      diameter=diameter,
      stroke_width=stroke_width,
    ),
  )
