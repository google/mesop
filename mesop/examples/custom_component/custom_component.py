from typing import Any, Callable

import mesop.labs as mel

# current_module_dir = os.path.dirname(os.path.abspath(__file__))
# js_file_path = os.path.join(current_module_dir, "custom_component.js")
# print(f"JS file path: {js_file_path}")


# mel.register_event_mapper(
#   IncrementEvent,
#   lambda event: IncrementEvent(key=event.key, value=event.json["value"]),
# )

# Instead of explicit event mapper.
# We will log the target event class when sending the event...
# Then, we will map the values to the class - key=key, othre attrs, based on key


@mel.web_component(path="./custom_component.js")
def foo_custom_component(
  *,
  value: int,
  on_increment: Callable[[mel.CustomEvent], Any],
  key: str | None = None,
):
  mel.insert_web_component(
    name="foo-component",
    key=key,
    events={
      "increment-event": on_increment,
    },
    properties={
      "value": value,
    },
  )
