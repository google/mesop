import mesop.components.icon.icon_pb2 as icon_pb
from mesop.component_helpers import Style, insert_component, to_style_proto
from mesop.utils.validate import validate


@validate
def icon(
  icon: str,
  *,
  key: str | None = None,
  style: Style | None = None,
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
    ),
    style=to_style_proto(style) if style else None,
  )
