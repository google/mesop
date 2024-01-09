from dataclasses import dataclass
from typing import Literal

import mesop.protos.ui_pb2 as pb


@dataclass(kw_only=True)
class BorderSide:
  width: int | str = 0
  color: str = ""
  style: Literal["none", "solid"] | None = None


@dataclass(kw_only=True)
class Border:
  top: BorderSide | None = None
  right: BorderSide | None = None
  bottom: BorderSide | None = None
  left: BorderSide | None = None


@dataclass(kw_only=True)
class EdgeInsets:
  top: int | str = 0
  right: int | str = 0
  bottom: int | str = 0
  left: int | str = 0


@dataclass(kw_only=True)
class Margin(EdgeInsets):
  pass


@dataclass(kw_only=True)
class Padding(EdgeInsets):
  pass


@dataclass(kw_only=True)
class Style:
  background: str = ""
  color: str = ""
  margin: Margin | None = None
  padding: Padding | None = None
  border: Border | None = None
  height: int | str = ""
  width: int | str = ""
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
  flex_grow: int = 0
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
    display=_str_or_none(s.display),
    flex_direction=_str_or_none(s.flex_direction),
    flex_grow=s.flex_grow,
    align_items=_str_or_none(s.align_items),
    position=_str_or_none(s.position),
    text_align=_str_or_none(s.text_align),
    border=_map_border(s.border),
  )


def _str_or_none(input: str | None) -> str:
  if input is None:
    return ""
  return input


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
  return pb.BorderSide(
    width=_px_str(bs.width), color=bs.color, style=_str_or_none(bs.style)
  )


def _px_str(int_or_str: int | str) -> str:
  if isinstance(int_or_str, int):
    return str(int_or_str) + "px"
  return int_or_str
