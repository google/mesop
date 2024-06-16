import mesop.components.embed.embed_pb2 as embed_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def embed(
  *,
  src: str,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates an embed component.

  Args:
      src: The source URL for the embed content.
      style: The style to apply to the embed, such as width and height.
      key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="embed",
    proto=embed_pb.EmbedType(src=src),
    style=style,
  )
