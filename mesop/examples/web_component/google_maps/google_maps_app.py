"""Proof of concept of a webcomponent wrapper that adds Google Maps support.
Note: Does not implement full interactions with a map. This is meant as a
    proof of concept that others can build upon for additional interactions with
    a web map.
"""

from typing import Tuple

from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.google_maps.google_maps_component import (
  google_maps_component,
)


@me.page(
  path="/google_maps_example",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",  # For Lit
      "https://maps.googleapis.com",  # For Google Maps API
    ],
    allowed_connect_srcs=[
      "https://maps.googleapis.com",  # For Google Maps API
    ],
    dangerously_disable_trusted_types=True,
  ),
)
def page():
  initial_center = (40.7128, -74.0060)  # New York City
  initial_zoom = 12

  markers_data = [
    {"latlng": (40.7128, -74.0060), "popup_content": "Marker 1: New York City"},
    {
      "latlng": (40.7488, -73.9857),
      "popup_content": "Marker 2: Empire State Building",
    },
  ]

  google_maps_component(
    center=initial_center,
    zoom=initial_zoom,
    markers=markers_data,
    on_click=on_map_click,
  )
  me.text(f"Map Clicked Location: {me.state(State).click_location}")


@me.stateclass
class State:
  click_location: str = "No click yet"


class MapClick(BaseModel):
  latlng: Tuple[float, float]


def on_map_click(e: mel.WebEvent):
  click = MapClick(**e.value)
  me.state(
    State
  ).click_location = (
    f"Latitude: {click.latlng[0]}, Longitude: {click.latlng[1]}"
  )
  print(f"Map clicked at: {click.latlng}")
