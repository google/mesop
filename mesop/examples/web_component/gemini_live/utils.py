from typing import Any, Callable

import mesop.labs as mel


def filter_events(events: dict[str, Callable[[mel.WebEvent], Any] | None]):
  """Helper function for filtering out web component events that do not have a callback."""
  return {event: callback for event, callback in events.items() if callback}
