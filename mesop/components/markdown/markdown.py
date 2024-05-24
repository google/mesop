from dataclasses import dataclass
from typing import Any, Callable

import markdown as markdown_lib
from markdown.extensions.codehilite import CodeHiliteExtension

import mesop.components.markdown.markdown_pb2 as markdown_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class MarkdownMenuSelectEvent(MesopEvent):
  """Event representing a change in the radio component's value.

  Attributes:
      value: The new value of the radio component after the change.
      key (str): key of the component that emitted this event.
  """

  value: str


register_event_mapper(
  MarkdownMenuSelectEvent,
  lambda event, key: MarkdownMenuSelectEvent(
    key=key.key, value=event.string_value
  ),
)


@register_native_component
def markdown(
  text: str | None = None,
  *,
  on_select: Callable[[MarkdownMenuSelectEvent], Any] | None = None,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a markdown.

  Args:
      text: **Required.** Markdown text
      style: Style to apply to component. Follows [HTML Element inline style API](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style).
  """

  if text:
    html = markdown_lib.markdown(
      text,
      extensions=[
        CodeHiliteExtension(css_class="highlight"),
        "fenced_code",
      ],
    )
  else:
    html = ""
  insert_component(
    key=key,
    type_name="markdown",
    style=style,
    proto=markdown_pb.MarkdownType(
      html=html,
      on_select_event_handler_id=register_event_handler(
        on_select, event=MarkdownMenuSelectEvent
      )
      if on_select
      else "",
    ),
  )
