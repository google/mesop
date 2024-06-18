import mesop.components.divider.divider_pb2 as divider_pb
from mesop.component_helpers import (
  insert_component,
  register_native_component,
)


@register_native_component
def divider(*, key: str | None = None, inset: bool = False):
  """Creates a Divider component.

  Args:
    key: The component [key](../components/index.md#component-key).
    inset: Whether the divider is an inset divider.
  """
  insert_component(
    key=key,
    type_name="divider",
    proto=divider_pb.DividerType(inset=inset),
  )
