from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.quickstart.counter_component import (
  counter_component,
)

# This is intended to repro a bug where loading stylesheet for a custom
# font would cause issues with the CSP and prevent web components
# from loading.
# https://github.com/google/mesop/issues/549


@me.page(
  path="/web_component/custom_font_csp_repro/custom_font_app",
  stylesheets=[
    "https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&family=Inter:wght@100..900&display=swap",
  ],
)
def page():
  me.text("Custom font: Inter Tight", style=me.Style(font_family="Inter Tight"))
  counter_component(
    value=me.state(State).value,
    on_decrement=on_decrement,
  )


@me.stateclass
class State:
  value: int = 10


class ChangeValue(BaseModel):
  value: int


def on_decrement(e: mel.WebEvent):
  # Creating a Pydantic model from the JSON value of the WebEvent
  # to enforce type safety.
  decrement = ChangeValue(**e.value)
  me.state(State).value = decrement.value
