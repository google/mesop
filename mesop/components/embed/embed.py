from typing import overload

import mesop.components.embed.embed_pb2 as embed_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@overload
def embed(
  *,
  src: str,
  style: Style | None = None,
  key: str | None = None,
) -> None:
  pass


@overload
def embed(
  *,
  html: str,
  style: Style | None = None,
  key: str | None = None,
) -> None:
  pass


@register_native_component
def embed(
  *,
  src: str | None = None,
  html: str | None = None,
  style: Style | None = None,
  key: str | None = None,
) -> None:
  """
  Creates an embed component.

  Either `src` _or_ `html` must be set, but not both.

  Args:
      src: The source URL for the embed content.
      html: The HTML document to use as the embedded content. This is treated as an iframe [srcdoc](https://developer.mozilla.org/en-US/docs/Web/API/HTMLIFrameElement/srcdoc).
      style: The style to apply to the embed, such as width and height.
      key: The component [key](../guides/components.md#component-key).
  """
  embed_proto = embed_pb.EmbedType()
  if src:
    embed_proto.src = src
  if html:
    embed_proto.html = html
  insert_component(
    key=key,
    type_name="embed",
    proto=embed_proto,
    style=style,
  )
