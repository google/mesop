from dataclasses import dataclass
from typing import Any, Callable, Literal

import mesop.components.slider.slider_pb2 as slider_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events.events import MesopEvent


@dataclass(kw_only=True)
class SliderValueChangeEvent(MesopEvent):
  """
  Event triggered when the slider value changes.

  Attributes:
      value: The new value of the slider after the change.
      key (str): Key of the component that emitted this event.
  """

  value: float


register_event_mapper(
  SliderValueChangeEvent,
  lambda event, key: SliderValueChangeEvent(
    key=key.key,
    value=event.double_value,
  ),
)


@register_native_component
def slider(
  *,
  on_value_change: Callable[[SliderValueChangeEvent], Any] | None = None,
  value: float | None = None,
  min: float = 0,
  max: float = 100,
  step: float = 1,
  color: Literal["primary", "accent", "warn"] = "primary",
  disabled: bool = False,
  discrete: bool = False,
  show_tick_marks: bool = False,
  disable_ripple: bool = False,
  style: Style | None = None,
  key: str | None = None,
):
  """Creates a Slider component.

  Args:
    on_value_change: An event will be dispatched each time the slider changes its value.
    value: Initial value. If updated, the slider will be updated with a new initial value.
    min: The minimum value that the slider can have.
    max: The maximum value that the slider can have.
    step: The values at which the thumb will snap.
    disabled: Whether the slider is disabled.
    discrete: Whether the slider displays a numeric value label upon pressing the thumb.
    show_tick_marks: Whether the slider displays tick marks along the slider track.
    color: Palette color of the slider.
    disable_ripple: Whether ripples are disabled in the slider.
    style: Style for the component.
    key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="slider",
    style=style,
    proto=slider_pb.SliderType(
      disabled=disabled,
      discrete=discrete,
      show_tick_marks=show_tick_marks,
      value=value if value is not None else min,
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
