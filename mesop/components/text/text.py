from typing import Literal

import mesop.components.text.text_pb2 as text_pb2
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def text(
  text: str | None = None,
  *,
  type: Literal[
    "headline-1",
    "headline-2",
    "headline-3",
    "headline-4",
    "headline-5",
    "headline-6",
    "subtitle-1",
    "subtitle-2",
    "body-1",
    "body-2",
    "caption",
    "button",
  ]
  | None = None,
  style: Style | None = None,
  key: str | None = None,
):
  """
  Create a text component.

  Args:
      text: The text to display.
      type: The typography level for the text.
      style: Style to apply to component. Follows [HTML Element inline style API](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style).
      key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="text",
    proto=text_pb2.TextType(
      text=text,
      type=type,
    ),
    style=style,
  )
