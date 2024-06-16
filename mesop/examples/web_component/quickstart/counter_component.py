from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./counter_component.js")
def counter_component(
  *,
  value: int,
  on_decrement: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="quickstart-counter-component",
    key=key,
    events={
      "decrementEvent": on_decrement,
    },
    properties={
      "value": value,
    },
  )
