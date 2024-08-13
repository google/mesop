from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./inner_component.js")
def inner_component(
  *,
  value: int,
  on_decrement: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
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
