from pydantic import validate_arguments

import mesop.components.icon.icon_pb2 as icon_pb
from mesop.component_helpers import (
  insert_component,
)


@validate_arguments
def icon(
  *,
  key: str | None = None,
  color: str = "",
  inline: bool = False,
  svg_icon: str = "",
  font_set: str = "",
  font_icon: str = "",
):
  """Creates a Icon component.

  Args:
    key: Unique identifier for this component instance.
    color: Theme palette color of the icon.
    inline: Whether the icon should be inlined, automatically sizing the icon to match the font size of the element the icon is contained in.
    svg_icon: Name of the icon in the SVG icon set.
    font_set: Font set that the icon is a part of.
    font_icon: Name of an icon within a font set.
  """
  insert_component(
    key=key,
    type_name="icon",
    proto=icon_pb.IconType(
      color=color,
      inline=inline,
      svg_icon=svg_icon,
      font_set=font_set,
      font_icon=font_icon,
    ),
  )
