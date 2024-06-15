from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./custom_component.js")
def foo_custom_component(
  *,
  disabled: bool,
  value: int,
  on_increment: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="foo-component",
    key=key,
    events={
      "increment-event": on_increment,
    },
    properties={
      "disabled": disabled,
      "value": value,
      "active": True,
    },
  )
