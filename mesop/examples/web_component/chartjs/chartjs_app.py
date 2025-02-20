import mesop as me
from mesop.examples.web_component.chartjs.chartjs_component import (
  chartjs_component,
)

_SUBTITLE_DATE = "Jan - May 2025"

_RED = "rgb(255, 99, 132)"
_BLUE = "rgb(54, 162, 235)"
_YELLOW = "rgb(255, 205, 86)"
_GREEN = "rgb(75, 192, 192)"
_GREY = "rgb(201, 203, 207)"

_DEFAULT_OPTIONS = {
  "responsive": True,
  "aspectRatio": 1,
  "maintainAspectRatio": True,
  "scales": {
    "y": {
      "beginAtZero": True,
    }
  },
}

_PIE_OPTIONS = {
  "options": {
    "plugins": {
      "legend": {
        "display": False,
      },
    },
    "responsive": True,
    "aspectRatio": 1,
    "maintainAspectRatio": True,
  },
}
_DOUGHNUT_OPTIONS = _PIE_OPTIONS
_POLAR_AREA_OPTIONS = (
  {
    "responsive": True,
    "aspectRatio": 1,
    "maintainAspectRatio": True,
    "scales": {
      "r": {
        "beginAtZero": True,
      }
    },
  },
)

config_line = {
  "type": "line",
  "data": {
    "labels": ["January", "February", "March", "April", "May"],
    "datasets": [
      {
        "label": "Pies",
        "data": [65, 59, 80, 81, 56],
        "backgroundColor": _RED,
        "borderColor": _RED,
        "fill": False,
      },
      {
        "label": "Donuts",
        "data": [102, 122, 115, 98, 128],
        "backgroundColor": _GREEN,
        "borderColor": _GREEN,
        "fill": False,
      },
    ],
  },
  "options": _DEFAULT_OPTIONS,
}

config_bar = {
  "type": "bar",
  "data": {
    "labels": ["January", "February", "March", "April", "May"],
    "datasets": [
      {
        "label": "Pies",
        "data": [65, 59, 80, 81, 56],
        "backgroundColor": _RED,
      },
      {
        "label": "Donuts",
        "data": [102, 122, 115, 98, 128],
        "backgroundColor": _GREEN,
      },
    ],
  },
  "options": _DEFAULT_OPTIONS,
}

config_area = {
  "type": "line",
  "data": {
    "labels": ["January", "February", "March", "April", "May"],
    "datasets": [
      {
        "label": "Pies",
        "data": [65, 59, 80, 81, 56],
        "backgroundColor": _RED,
        "borderColor": _RED,
        "fill": True,
      },
      {
        "label": "Donuts",
        "data": [102, 122, 115, 98, 128],
        "backgroundColor": _GREEN,
        "borderColor": _GREEN,
        "fill": True,
      },
    ],
  },
  "options": _DEFAULT_OPTIONS,
}

config_doughnut = {
  "type": "doughnut",
  "data": {
    "labels": ["Apple fritter", "Glazed", "Bear claw", "Cruller"],
    "datasets": [
      {
        "data": [300, 50, 100, 42],
        "backgroundColor": [
          _RED,
          _BLUE,
          _YELLOW,
          _GREEN,
        ],
        "hoverOffset": 4,
      }
    ],
  },
  "options": _DOUGHNUT_OPTIONS,
}

config_pie = {
  "type": "pie",
  "data": {
    "labels": ["Lemon Meringue", "Pumpkin", "Apple", "Banana Cream"],
    "datasets": [
      {
        "data": [300, 50, 100, 42],
        "backgroundColor": [
          _RED,
          _BLUE,
          _YELLOW,
          _GREEN,
        ],
        "hoverOffset": 4,
      }
    ],
  },
  "options": _PIE_OPTIONS,
}

config_polar_area = {
  "type": "polarArea",
  "data": {
    "labels": ["Pies", "Donuts", "Cakes", "Cookies", "Brownies"],
    "datasets": [
      {
        "label": "Dessert Sales",
        "data": [11, 16, 7, 3, 14],
        "backgroundColor": [
          _RED,
          _GREEN,
          _YELLOW,
          _GREY,
          _BLUE,
        ],
      }
    ],
  },
  "options": _POLAR_AREA_OPTIONS,
}


@me.page(
  path="/web_component/chartjs/chartjs_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
      "https://cdn.jsdelivr.net/npm/chart.js",
    ]
  ),
)
def page():
  with me.box(
    style=me.Style(
      margin=me.Margin.all(15), display="flex", gap=15, flex_wrap="wrap"
    )
  ):
    with me.card():
      me.card_header(title="Bar Chart", subtitle=_SUBTITLE_DATE)
      with me.card_content():
        chartjs_component(config=config_bar)

    with me.card():
      me.card_header(title="Line Chart", subtitle=_SUBTITLE_DATE)
      with me.card_content():
        chartjs_component(config=config_line)

    with me.card():
      me.card_header(title="Area Chart", subtitle=_SUBTITLE_DATE)
      with me.card_content():
        chartjs_component(config=config_area)

    with me.card():
      me.card_header(title="Donut Chart", subtitle=_SUBTITLE_DATE)
      with me.card_content():
        chartjs_component(config=config_doughnut)

    with me.card():
      me.card_header(title="Pie Chart", subtitle=_SUBTITLE_DATE)
      with me.card_content():
        chartjs_component(config=config_pie)

    with me.card():
      me.card_header(title="Polar Area Chart", subtitle=_SUBTITLE_DATE)
      with me.card_content():
        chartjs_component(config=config_polar_area)
