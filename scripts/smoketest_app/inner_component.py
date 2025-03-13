from typing import Any, Callable

import mesop as me


@me.web_component(path="./inner_component.js")
def inner_component(
  *,
  value: int,
  on_decrement: Callable[[me.WebEvent], Any],
  key: str | None = None,
):
  return me.insert_web_component(
    name="inner-component",
    key=key,
    events={
      "decrementEvent": on_decrement,
    },
    properties={
      "value": value,
      "active": True,
    },
  )
