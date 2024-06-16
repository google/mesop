import mesop.components.icon.icon_pb2 as icon_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def icon(
  icon: str | None = None,
  *,
  key: str | None = None,
  style: Style | None = None,
):
  """Creates a Icon component.

  Args:
    key: The component [key](../components/index.md#component-key).
    icon: Name of the [Material Symbols icon](https://fonts.google.com/icons).
    style: Inline styles
  """
  insert_component(
    key=key,
    type_name="icon",
    proto=icon_pb.IconType(
      icon=icon,
    ),
    style=style,
  )
