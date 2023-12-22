import mesop.components.icon.icon_pb2 as icon_pb
from mesop.component_helpers import (
  insert_component,
)
from mesop.utils.validate import validate


@validate
def icon(
  icon: str,
  *,
  key: str | None = None,
  style: str = "",
):
  """Creates a Icon component.

  Args:
    key: Unique identifier for this component instance.
    icon: Name of the [Material Symbols icon](https://fonts.google.com/icons).
    style: Inline styles
  """
  insert_component(
    key=key,
    type_name="icon",
    proto=icon_pb.IconType(
      font_icon=icon,
      style=style,
    ),
  )
