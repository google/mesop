import mesop.components.html.html_pb2 as html_pb
from mesop.component_helpers import (
  Border,
  BorderSide,
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def html(
  html: str = "",
  *,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function renders custom HTML inside an iframe for web security isolation.

  Args:
      html: The HTML content to be rendered.
      style: The style to apply to the embed, such as width and height.
      key: The component [key](../components/index.md#component-key).
  """
  if style is None:
    style = Style()
  if style.border is None:
    style.border = Border.all(
      BorderSide(
        width=0,
      )
    )
  insert_component(
    key=key,
    type_name="html",
    proto=html_pb.HtmlType(
      html=html,
    ),
    style=style,
  )
