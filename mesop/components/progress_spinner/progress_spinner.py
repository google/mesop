import mesop.components.progress_spinner.progress_spinner_pb2 as progress_spinner_pb
from mesop.component_helpers import (
  insert_component,
  register_component,
)


@register_component
def progress_spinner(
  *,
  key: str | None = None,
  color: str = "",
  diameter: float = 100,
  stroke_width: float = 10,
):
  """Creates a Progress spinner component.

  Args:
    key: Unique identifier for this component instance.
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
