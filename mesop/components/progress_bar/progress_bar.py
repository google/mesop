from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.progress_bar.progress_bar_pb2 as progress_bar_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class ProgressBarAnimationEndEvent(MesopEvent):
  """
  Event emitted when the animation of the progress bar ends.

  Attributes:
      value: The value of the progress bar when the animation ends.
      key (str): Key of the component that emitted this event.
  """

  value: float


register_event_mapper(
  ProgressBarAnimationEndEvent,
  lambda event, key: ProgressBarAnimationEndEvent(
    key=key.key,
    value=event.double_value,
  ),
)


@register_native_component
def progress_bar(
  *,
  key: str | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  value: float = 0,
  buffer_value: float = 0,
  mode: Literal[
    "determinate", "indeterminate", "buffer", "query"
  ] = "indeterminate",
  on_animation_end: Callable[[ProgressBarAnimationEndEvent], Any] | None = None,
):
  """Creates a Progress bar component.

  Args:
    key: The component [key](../components/index.md#component-key).
    color: Theme palette color of the progress bar.
    value: Value of the progress bar. Defaults to zero. Mirrored to aria-valuenow.
    buffer_value: Buffer value of the progress bar. Defaults to zero.
    mode: Mode of the progress bar. Input must be one of these values: determinate, indeterminate, buffer, query, defaults to 'determinate'. Mirrored to mode attribute.
    on_animation_end: Event emitted when animation of the primary progress bar completes. This event will not be emitted when animations are disabled, nor will it be emitted for modes with continuous animations (indeterminate and query).
  """
  insert_component(
    key=key,
    type_name="progress_bar",
    proto=progress_bar_pb.ProgressBarType(
      color=color,
      value=value,
      buffer_value=buffer_value,
      mode=mode,
      on_progress_bar_animation_end_event_handler_id=register_event_handler(
        on_animation_end, event=ProgressBarAnimationEndEvent
      )
      if on_animation_end
      else "",
    ),
  )
