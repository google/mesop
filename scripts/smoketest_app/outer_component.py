from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./outer_component.js")
def outer_component(
  *,
  value: int,
  on_increment: Callable[[mel.CustomEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="outer-component",
    key=key,
    events={
      "increment-event": on_increment,
    },
    properties={
      "value": value,
      "active": True,
    },
  )
