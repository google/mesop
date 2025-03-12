from typing import Any, Callable

import mesop as me


@me.web_component(path="./outer_component.js")
def outer_component(
  *,
  value: int,
  on_increment: Callable[[me.WebEvent], Any],
  key: str | None = None,
):
  return me.insert_web_component(
    name="outer-component",
    key=key,
    events={
      "incrementEvent": on_increment,
    },
    properties={
      "value": value,
      "active": True,
    },
  )
