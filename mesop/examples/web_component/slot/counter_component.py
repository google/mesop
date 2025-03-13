from typing import Any, Callable

import mesop as me


@me.web_component(path="./counter_component.js")
def counter_component(
  *,
  value: int,
  on_decrement: Callable[[me.WebEvent], Any],
  key: str | None = None,
):
  return me.insert_web_component(
    name="slot-counter-component",
    key=key,
    events={
      "decrementEvent": on_decrement,
    },
    properties={
      "value": value,
    },
  )
