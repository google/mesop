import mesop.components.sidenav.sidenav_pb2 as sidenav_pb
from mesop.component_helpers import (
  Style,
  insert_composite_component,
  register_native_component,
)


@register_native_component
def sidenav(
  *,
  opened: bool = True,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a sidenav.

  Args:
      opened: A flag to determine if the sidenav is open or closed. Defaults to True.
      style: An optional Style object to apply custom styles. Defaults to None.
      key: The component [key](../components/index.md#component-key).
  """
  return insert_composite_component(
    key=key,
    type_name="sidenav",
    style=style,
    proto=sidenav_pb.SidenavType(
      opened=opened,
    ),
  )
