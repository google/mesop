from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.slider.slider_pb2 as slider_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
)
from mesop.events.events import MesopEvent
from mesop.utils.validate import validate


@dataclass
class SliderValueChangeEvent(MesopEvent):
  value: float


register_event_mapper(
  SliderValueChangeEvent,
  lambda event, key: SliderValueChangeEvent(
    key=key.key,
    value=event.double,
  ),
)


@validate
def slider(
  *,
  key: str | None = None,
  disabled: bool = False,
  discrete: bool = False,
  show_tick_marks: bool = False,
  min: float = 0,
  color: Literal["primary", "accent", "warn"] = "primary",
  disable_ripple: bool = False,
  max: float = 100,
  step: float = 1,
  on_value_change: Callable[[SliderValueChangeEvent], Any] | None = None,
):
  """Creates a Slider component.

  Args:
    key: Unique identifier for this component instance.
    disabled: Whether the slider is disabled.
    discrete: Whether the slider displays a numeric value label upon pressing the thumb.
    show_tick_marks: Whether the slider displays tick marks along the slider track.
    min: The minimum value that the slider can have.
    color: Palette color of the slider.
    disable_ripple: Whether ripples are disabled in the slider.
    max: The maximum value that the slider can have.
    step: The values at which the thumb will snap.
    on_value_change: An event will be dispatched each time the slider changes its value.
  """
  insert_component(
    key=key,
    type_name="slider",
    proto=slider_pb.SliderType(
      disabled=disabled,
      discrete=discrete,
      show_tick_marks=show_tick_marks,
      min=min,
      color=color,
      disable_ripple=disable_ripple,
      max=max,
      step=step,
      on_value_change_handler_id=register_event_handler(
        on_value_change, SliderValueChangeEvent
      )
      if on_value_change
      else "",
    ),
  )
