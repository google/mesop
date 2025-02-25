import json
import os
from typing import Callable, Literal

from google import genai  # type: ignore
from google.genai import types
from pydantic import BaseModel

import mesop as me
from mesop.examples.web_component.chartjs.chartjs_chat import (
  ChatMessage,
  ResponseType,
  chartjs_chat,
)
from mesop.examples.web_component.chartjs.chartjs_component import (
  chartjs_component,
)

RESPONSE_TYPE_CHARTJS = "chartjs"

_RED = "rgb(255, 99, 132)"
_BLUE = "rgb(54, 162, 235)"
_YELLOW = "rgb(255, 205, 86)"
_GREEN = "rgb(75, 192, 192)"
_GREY = "rgb(201, 203, 207)"

_COLORS = [_RED, _BLUE, _YELLOW, _GREEN, _GREY]


class ChartJsDataset(BaseModel):
  label: str
  data: list[float]


class ChartJsData(BaseModel):
  labels: list[str]
  datasets: list[ChartJsDataset]


class ChartJsConfig(BaseModel):
  type: Literal["line", "bar", "doughnut", "pie"]
  data: ChartJsData


@me.stateclass
class State:
  api_key: str = os.getenv("GOOGLE_API_KEY", "")
  dialog_is_open: bool = True


@me.page(
  path="/web_component/chartjs/chartjs_chat_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
      "https://cdn.jsdelivr.net/npm/chart.js",
    ]
  ),
  title="Mesop Chart.js Chat Demo",
)
def page():
  api_key_dialog()
  chartjs_chat(
    transform,
    title="Mesop Chart.js Chat Demo",
    bot_user="Mesop Bot",
    custom_response_renderers={
      RESPONSE_TYPE_CHARTJS: render_chartjs,
    },
  )


def api_key_dialog():
  state = me.state(State)
  with dialog(
    is_open=state.dialog_is_open,
    on_click_background=on_click_close_background,
  ):
    with me.box():
      me.text("A Google API key is needed for this demo.", type="headline-6")
      me.input(
        label="Google API key",
        type="password",
        on_blur=on_blur,
        style=me.Style(width="100%"),
      )
    with dialog_actions():
      me.button("Done", on_click=on_click_close_dialog)


def transform(input: str, history: list[ChatMessage]):
  state = me.state(State)
  client = genai.Client(api_key=state.api_key)
  response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=input,
    config=types.GenerateContentConfig(
      response_mime_type="application/json",
      response_schema=ChartJsConfig,
    ),
  )
  return ResponseType(
    type=RESPONSE_TYPE_CHARTJS,
    content=response.text,
  )


def get_color(index: int, colors: list[str]) -> str:
  if 0 <= index < len(colors):
    return colors[index]
  return colors[-1]


def get_chart_options(chart_type: str):
  font_color = "#777" if me.theme_brightness() == "light" else "#ddd"
  default = {
    "responsive": True,
    "aspectRatio": 2,
    "maintainAspectRatio": True,
    "scales": {
      "x": {"grid": {"display": False}, "ticks": {"color": font_color}},
      "y": {
        "ticks": {"color": font_color},
        "beginAtZero": True,
      },
    },
    "plugins": {
      "legend": {"labels": {"color": font_color}},
      "tooltip": {
        "backgroundColor": "#1F2937",
        "titleColor": "#F3F4F6",
        "bodyColor": "#F3F4F6",
        "borderColor": "#374151",
        "borderWidth": 1,
      },
    },
  }

  pie = {
    "responsive": True,
    "aspectRatio": 2,
    "maintainAspectRatio": True,
  }
  doughnut = pie

  chart_mapping = {
    "doughnut": doughnut,
    "pie": pie,
  }
  return chart_mapping.get(chart_type, default)


def make_graph(config: ChartJsConfig):
  colors = list(_COLORS)
  datasets = []
  if config.type == "line":
    for index, dataset in enumerate(config.data.datasets):
      color = get_color(index, colors)
      datasets.append(
        {
          "label": dataset.label,
          "data": dataset.data,
          "backgroundColor": color,
          "borderColor": color,
          "fill": False,
        }
      )
  elif config.type == "bar":
    for index, dataset in enumerate(config.data.datasets):
      color = get_color(index, colors)
      datasets.append(
        {
          "label": dataset.label,
          "data": dataset.data,
          "backgroundColor": color,
        }
      )
  elif config.type in {"doughnut", "pie"}:
    for dataset in config.data.datasets:
      datasets.append(
        {
          "label": dataset.label,
          "data": dataset.data,
          "backgroundColor": colors,
          "hoverOffset": 4,
        }
      )

  return {
    "type": config.type,
    "data": {
      "labels": config.data.labels,
      "datasets": datasets,
    },
    "options": get_chart_options(config.type),
  }


def render_chartjs(input: str):
  chartjs_component(config=make_graph(ChartJsConfig(**json.loads(input))))


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.api_key = e.value


def on_click_close_background(e: me.ClickEvent):
  state = me.state(State)
  if e.is_target:
    state.dialog_is_open = False


def on_click_close_dialog(e: me.ClickEvent):
  state = me.state(State)
  state.dialog_is_open = False


@me.content_component
def dialog(*, is_open: bool, on_click_background: Callable | None = None):
  """Renders a dialog component.

  The design of the dialog borrows from the Angular component dialog. So basically
  rounded corners and some box shadow.

  Args:
    is_open: Whether the dialog is visible or not.
    on_click_background: Event handler for when background is clicked
  """
  with me.box(
    style=me.Style(
      background="rgba(0, 0, 0, 0.4)"
      if me.theme_brightness() == "light"
      else "rgba(255, 255, 255, 0.4)",
      display="block" if is_open else "none",
      height="100%",
      overflow_x="auto",
      overflow_y="auto",
      position="fixed",
      width="100%",
      z_index=1000,
    ),
  ):
    with me.box(
      on_click=on_click_background,
      style=me.Style(
        place_items="center",
        display="grid",
        height="100vh",
      ),
    ):
      with me.box(
        style=me.Style(
          background=me.theme_var("surface-container-lowest"),
          border_radius=20,
          box_sizing="content-box",
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
          padding=me.Padding.all(20),
        )
      ):
        me.slot()


@me.content_component
def dialog_actions():
  """Helper component for rendering action buttons so they are right aligned.

  This component is optional. If you want to position action buttons differently,
  you can just write your own Mesop markup.
  """
  with me.box(
    style=me.Style(
      display="flex", justify_content="end", gap=5, margin=me.Margin(top=20)
    )
  ):
    me.slot()
