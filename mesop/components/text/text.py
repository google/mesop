from enum import Enum
from typing import cast

import mesop.components.text.text_pb2 as text_pb2
from mesop.component_helpers import insert_component
from mesop.utils.validate import validate


# Must be kept in sync with enum in text.proto
class Typography(Enum):
  TYPOGRAPHY_UNSET = 0
  H1 = 1
  H2 = 2
  H3 = 3
  H4 = 4
  H5 = 5
  H6 = 6
  SUBTITLE1 = 7
  SUBTITLE2 = 8
  BODY1 = 9
  BODY2 = 10
  CAPTION = 11


@validate
def text(
  text: str,
  *,
  type: Typography = Typography.TYPOGRAPHY_UNSET,
  style: str = "",
  key: str | None = None,
):
  """
  Create a text component.

  Args:
      text: The text to display.
      type: The typography level for the text.
      style: Style to apply to component. Follows [HTML Element inline style API](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style).
      key: An optional key to uniquely identify the component. Defaults to None.

  """
  # The Python and Proto enum values should be exactly 1:1
  typography_level = cast(
    text_pb2.TextType.TypographyLevel.ValueType, type.value
  )
  insert_component(
    key=key,
    type_name="text",
    proto=text_pb2.TextType(
      text=text, typography_level=typography_level, style=style
    ),
  )
