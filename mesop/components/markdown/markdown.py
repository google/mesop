import mesop.components.markdown.markdown_pb2 as markdown_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def markdown(
  text: str | None = None,
  *,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a markdown.

  Args:
      text: **Required.** Markdown text
      style: Style to apply to component. Follows [HTML Element inline style API](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style).
  """
  insert_component(
    key=key,
    type_name="markdown",
    style=style,
    proto=markdown_pb.MarkdownType(
      text=text or "",
    ),
  )
