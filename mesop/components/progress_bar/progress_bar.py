from dataclasses import dataclass
from typing import Any, Callable, Literal

from pydantic import validate_arguments

import mesop.components.progress_bar.progress_bar_pb2 as progress_bar_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
)
from mesop.events import MesopEvent


@dataclass
class ProgressBarAnimationEndEvent(MesopEvent):
  value: float


register_event_mapper(
  ProgressBarAnimationEndEvent,
  lambda event, key: ProgressBarAnimationEndEvent(
    key=key.key,
    value=event.double,
  ),
)


@validate_arguments
def progress_bar(
  *,
  key: str | None = None,
  color: str = "",
  value: float = 0,
  buffer_value: float = 0,
  mode: Literal[
    "determinate", "indeterminate", "buffer", "query"
  ] = "determinate",
  on_animation_end: Callable[[ProgressBarAnimationEndEvent], Any] | None = None,
):
  """Creates a Progress bar component.

  Args:
    key: Unique identifier for this component instance.
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
