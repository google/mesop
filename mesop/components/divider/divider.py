import mesop.components.divider.divider_pb2 as divider_pb
from mesop.component_helpers import (
  insert_component,
  register_component,
)


@register_component
def divider(
  *, key: str | None = None, vertical: bool = False, inset: bool = False
):
  """Creates a Divider component.

  Args:
    key: Unique identifier for this component instance.
    vertical: Whether the divider is vertically aligned.
    inset: Whether the divider is an inset divider.
  """
  insert_component(
    key=key,
    type_name="divider",
    proto=divider_pb.DividerType(vertical=vertical, inset=inset),
  )
