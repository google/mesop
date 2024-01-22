from dataclasses import dataclass
from typing import Literal

import mesop.protos.ui_pb2 as pb

OverflowValues = Literal["visible", "hidden", "clip", "scroll", "auto"]


@dataclass(kw_only=True)
class BorderSide:
  """
  Represents the style of a single side of a border in a UI component.

  Attributes:
      width: The width of the border. Can be specified as an integer value representing pixels,
                                a string with a unit (e.g., '2em'), or None for no width.
      color: The color of the border, represented as a string. This can be any valid CSS color value,
                          or None for no color.
      style: The style of the border, which can be 'none' for no border, 'solid' for a solid line.
  """

  width: int | str | None = None
  color: str | None = None
  style: Literal["none", "solid"] | None = None


@dataclass(kw_only=True)
class Border:
  """
  Defines the border styles for each side of a UI component.

  Attributes:
      top: Style for the top border.
      right: Style for the right border.
      bottom: Style for the bottom border.
      left: Style for the left border.
  """

  top: BorderSide | None = None
  right: BorderSide | None = None
  bottom: BorderSide | None = None
  left: BorderSide | None = None


@dataclass(kw_only=True)
class _EdgeInsets:
  top: int | str | None = None
  right: int | str | None = None
  bottom: int | str | None = None
  left: int | str | None = None


@dataclass(kw_only=True)
class Margin(_EdgeInsets):
  """
  Defines the margin space around a UI component.

  Attributes:
      top: Top margin (note: `2` is the same as `2px`)
      right: Right margin
      bottom: Bottom margin
      left: Left margin
  """

  top: int | str | None = None
  right: int | str | None = None
  bottom: int | str | None = None
  left: int | str | None = None


@dataclass(kw_only=True)
class Padding(_EdgeInsets):
  """
  Defines the padding space around a UI component.

  Attributes:
      top: Top padding (note: `2` is the same as `2px`)
      right: Right padding
      bottom: Bottom padding
      left: Left padding
  """

  top: int | str | None = None
  right: int | str | None = None
  bottom: int | str | None = None
  left: int | str | None = None


@dataclass(kw_only=True)
class Style:
  """
  Represents the style configuration for a UI component.

  Attributes:
      align_items: Specifies the default alignment for items inside a flexible container. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items).
      background: Sets the background color or image of the component. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/background).
      border: Defines the border properties for each side of the component. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/border).
      color: Sets the color of the text inside the component. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/color).
      columns: Specifies the number of columns in a multi-column element. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/columns).
      display: Defines the display type of the component. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/display).
      flex_basis: Specifies the initial length of a flexible item. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-basis).
      flex_direction: Establishes the main-axis, thus defining the direction flex items are placed in the flex container. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-direction).
      flex_grow: Defines the ability for a flex item to grow if necessary. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-grow).
      flex_shrink: Defines the ability for a flex item to shrink if necessary. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-shrink).
      flex_wrap: Allows flex items to wrap onto multiple lines. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-wrap).
      font_size: Sets the size of the font. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size).
      font_style: Specifies the font style for text. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/font-style).
      font_weight: Sets the weight (or boldness) of the font. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight).
      height: Sets the height of the component. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/height).
      justify_content: Aligns the flexible container's items when the items do not use all available space on the main-axis. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content).
      letter_spacing: Increases or decreases the space between characters in text. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/letter-spacing).
      margin: Sets the margin space required on each side of an element. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/margin).
      overflow_x: Specifies the handling of overflow in the horizontal direction. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-x).
      overflow_y: Specifies the handling of overflow in the vertical direction. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-y).
      padding: Sets the padding space required on each side of an element. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/padding).
      position: Specifies the type of positioning method used for an element (static, relative, absolute, fixed, or sticky). See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/position).
      text_align: Specifies the horizontal alignment of text in an element. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/text-align).
      text_decoration: Specifies the decoration added to text. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration).
      text_overflow: Specifies how overflowed content that is not displayed should be signaled to the user. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/text-overflow).
      white_space: Specifies how white space inside an element is handled. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space).
      width: Sets the width of the component. See [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/width).
  """

  # For literal properties, make the most commonly used option the first literal
  # element, as it will be used as the default value by the editor when creating that property.

  align_items: Literal[
    "normal",
    "stretch",
    "center",
    "start",
    "end",
  ] | None = None
  background: str | None = None
  border: Border | None = None
  color: str | None = None
  columns: int | None = None
  display: Literal[
    # precomposed values
    "block",
    "inline",
    "inline-block",
    "flex",
    "inline-flex",
    "grid",
    "inline-grid",
    # box generation
    "none",
    "contents",
  ] | None = None
  flex_basis: str | None = None
  flex_direction: Literal[
    "row",
    "row-reverse",
    "column",
    "column-reverse",
  ] | None = None
  flex_grow: int | None = None
  flex_shrink: int | None = None
  flex_wrap: Literal["nowrap", "wrap", "wrap-reverse"] | None = None
  font_size: int | str | None = None
  font_style: Literal["italic", "normal"] | None = None
  font_weight: Literal[
    "bold",
    "normal",
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900,
  ] | None = None
  height: int | str | None = None
  justify_content: Literal[
    "center",
    "start",
    "end",
    "flex",
    "flex",
    "left",
    "right",
  ] | None = None
  letter_spacing: int | str | None = None
  margin: Margin | None = None
  overflow_x: OverflowValues | None = None
  overflow_y: OverflowValues | None = None
  padding: Padding | None = None
  position: Literal[
    "static",
    "relative",
    "absolute",
    "fixed",
    "sticky",
  ] | None = None
  text_align: Literal[
    "start",
    "end",
    "left",
    "right",
    "center",
  ] | None = None
  text_decoration: Literal["underline", "none"] | None = None
  text_overflow: Literal["ellipsis", "clip"] | None = None
  white_space: Literal[
    "normal",
    "nowrap",
    "pre",
    "pre-wrap",
    "pre-line",
    "break-spaces",
  ] | None = None
  width: int | str | None = None


def to_style_proto(s: Style) -> pb.Style:
  return pb.Style(
    align_items=s.align_items,
    background=s.background,
    border=_map_border(s.border),
    color=s.color,
    columns=s.columns,
    display=s.display,
    flex_basis=s.flex_basis,
    flex_direction=s.flex_direction,
    flex_grow=s.flex_grow,
    flex_shrink=s.flex_shrink,
    flex_wrap=s.flex_wrap,
    font_size=_px_str(s.font_size),
    font_style=s.font_style,
    font_weight=_map_font_weight(s.font_weight),
    height=_px_str(s.height),
    justify_content=s.justify_content,
    letter_spacing=_px_str(s.letter_spacing),
    margin=_map_edge_insets(s.margin),
    overflow_x=s.overflow_x,
    overflow_y=s.overflow_y,
    padding=_map_edge_insets(s.padding),
    position=s.position,
    text_align=s.text_align,
    text_decoration=s.text_decoration,
    text_overflow=s.text_overflow,
    white_space=s.white_space,
    width=_px_str(s.width),
  )


def _map_font_weight(fw: int | str | None) -> str:
  if fw is None:
    return ""
  return str(fw)


def _map_edge_insets(e: _EdgeInsets | None) -> pb.EdgeInsets | None:
  if e is None:
    return None
  return pb.EdgeInsets(
    top=_px_str(e.top),
    bottom=_px_str(e.bottom),
    left=_px_str(e.left),
    right=_px_str(e.right),
  )


def _map_border(b: Border | None) -> pb.Border | None:
  if b is None:
    return None
  return pb.Border(
    top=_map_border_side(b.top),
    bottom=_map_border_side(b.bottom),
    left=_map_border_side(b.left),
    right=_map_border_side(b.right),
  )


def _map_border_side(bs: BorderSide | None) -> pb.BorderSide | None:
  if bs is None:
    return None
  return pb.BorderSide(width=_px_str(bs.width), color=bs.color, style=bs.style)


def _px_str(int_or_str: int | str | None) -> str | None:
  if isinstance(int_or_str, int):
    return str(int_or_str) + "px"
  return int_or_str
