import json
import os
from dataclasses import dataclass
from typing import Any, Callable

import mesop as me

current_module_dir = os.path.dirname(os.path.abspath(__file__))
js_file_path = os.path.join(current_module_dir, "custom_component.js")
print(f"JS file path: {js_file_path}")


@dataclass(kw_only=True)
class CustomEvent(me.UserEvent):
  value: int


me.register_event_mapper(
  CustomEvent,
  lambda event, key: CustomEvent(
    key=key.key, value=json.loads(event.string_value)["value"]
  ),
)


@me.web_component(js_path=js_file_path)
def foo_custom_component(
  *,
  value: int,
  on_event: Callable[..., Any],
  key: str | None = None,
  style: me.Style | None = None,
):
  me.insert_web_component(
    name="foo-component",
    key=key,
    style=style,
    properties={
      "value": value,
      "handler-id": me.register_event_handler(on_event, CustomEvent),
    },
  )
  pass
