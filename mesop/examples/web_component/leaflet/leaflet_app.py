"""Proof of concept of a webcomponent wrapper that adds Leaflet map support.

Note: Does not implement full interactions with a map. This is meant as a
    proof of concept that others can build upon for additional interactions with
    a web map.
"""

# app.py
from typing import Tuple

from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.leaflet.leaflet_component import (
  leaflet_map_component,
)


@me.page(
  path="/leaflet_map_example",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",  # For Lit and Leaflet
      "https://unpkg.com",  # For Leaflet CSS and JS
    ],
    dangerously_disable_trusted_types=True,
  ),
  stylesheets=[
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
  ],
)
def page():
  initial_center = (51.505, -0.09)  # London
  initial_zoom = 13

  markers_data = [
    {"latlng": (51.5, -0.1), "popup_content": "Marker 1: London Eye"},
    {"latlng": (51.51, -0.08), "popup_content": "Marker 2: Tower Bridge"},
  ]

  leaflet_map_component(
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
