from typing import Literal

import mesop.components.link.link_pb2 as link_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def link(
  *,
  text: str,
  url: str,
  target: Literal["_self", "_blank", "_parent", "_top"] = "_self",
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a link.

  Args:
      text: The text to be displayed
      url: The URL to navigate to
      style: Style for the component.
  """
  insert_component(
    key=key,
    style=style,
    type_name="link",
    proto=link_pb.LinkType(
      target=target,
      text=text,
      url=url,
    ),
  )
