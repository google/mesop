from dataclasses import dataclass
from typing import Literal

import mesop.protos.ui_pb2 as pb


@dataclass(kw_only=True)
class BorderSide:
  width: int | str | None = None
  color: str | None = None
  style: Literal["none", "solid"] | None = None


@dataclass(kw_only=True)
class Border:
  top: BorderSide | None = None
  right: BorderSide | None = None
  bottom: BorderSide | None = None
  left: BorderSide | None = None


@dataclass(kw_only=True)
class EdgeInsets:
  top: int | str | None = None
  right: int | str | None = None
  bottom: int | str | None = None
  left: int | str | None = None


@dataclass(kw_only=True)
class Margin(EdgeInsets):
  pass


@dataclass(kw_only=True)
class Padding(EdgeInsets):
  pass


@dataclass(kw_only=True)
class Style:
  background: str | None = None
  color: str | None = None
  font_size: int | str | None = None
  font_weight: Literal[
    "normal",
    "bold",
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
  margin: Margin | None = None
  padding: Padding | None = None
  border: Border | None = None
  height: int | str | None = None
  width: int | str | None = None
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
  flex_direction: Literal[
    "row",
    "row-reverse",
    "column",
    "column-reverse",
  ] | None = None
  flex_grow: int | None = None
  align_items: Literal[
    "normal",
    "stretch",
    "center",
    "start",
    "end",
  ] | None = None
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


def to_style_proto(s: Style) -> pb.Style:
  return pb.Style(
    background=s.background,
    color=s.color,
    height=_px_str(s.height),
    width=_px_str(s.width),
    margin=_map_edge_insets(s.margin),
    padding=_map_edge_insets(s.padding),
    display=s.display,
    flex_direction=s.flex_direction,
    flex_grow=s.flex_grow,
    align_items=s.align_items,
    position=s.position,
    text_align=s.text_align,
    border=_map_border(s.border),
    font_weight=_map_font_weight(s.font_weight),
    font_size=_px_str(s.font_size),
  )


def _map_font_weight(fw: int | str | None) -> str:
  if fw is None:
    return ""
  return str(fw)


def _map_edge_insets(e: EdgeInsets | None) -> pb.EdgeInsets | None:
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
