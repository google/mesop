# google_maps_component.py
from typing import Any, Callable, Dict, List, Tuple

import mesop.labs as mel


@mel.web_component(path="./google_maps_component.js")
def google_maps_component(
  *,
  center: Tuple[float, float] = (0.0, 0.0),  # [latitude, longitude]
  zoom: int = 13,
  markers: List[Dict[str, Any]] | None = None,  # List of marker objects
  on_click: Callable[[mel.WebEvent], Any] | None = None,
  key: str | None = None,
):
  """
  A web component wrapper for a Google Map.

  Args:
      center: Initial map center as a tuple (latitude, longitude).
      zoom: Initial map zoom level.
      markers: A list of marker objects, each a dictionary with keys:
          - latlng: Tuple (latitude, longitude) for marker position.
          - popup_content: String content for the marker's popup (optional).
      on_click: Callback function when the map is clicked (optional).
      key: Unique key for the component.
  """
  events = {"clickEvent": on_click}

  properties = {
    "center": center,
    "zoom": zoom,
    "markers": markers
    if markers
    else [],  # Ensure markers is always a list (empty if None)
  }

  return mel.insert_web_component(
    name="google-maps-component",
    key=key,
    events=events,
    properties=properties,
  )
