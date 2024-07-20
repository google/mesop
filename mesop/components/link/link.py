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
  open_in_new_tab: bool = False,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a link.

  Args:
      text: The text to be displayed.
      url: The URL to navigate to.
      open_in_new_tab: If True, open page in new tab. If False, open page in current tab.
      style: Style for the component. Defaults to None.
      key: Unique key for the component. Defaults to None.
  """
  insert_component(
    key=key,
    style=style,
    type_name="link",
    proto=link_pb.LinkType(
      target="_blank" if open_in_new_tab else "_self",
      text=text,
      url=url,
    ),
  )
