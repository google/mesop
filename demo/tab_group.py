"""Simple tab group example.

- Use this code as a starting point for creating tab group-like functionlity.
- Extend/Modify it for your specific use case.
"""

from dataclasses import dataclass, field
from typing import Callable

import mesop as me


@dataclass
class Tab:
  label: str
  content: Callable
  selected: bool = False
  disabled: bool = False
  icon: str | None = None


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.stateclass
class State:
  selected_tab_index: int = 0
  disabled_tab_indexes: set[int] = field(default_factory=lambda: {1})


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/tab_group",
)
def app():
  with me.box():
    tab_group(make_tabs(), on_tab_click)


def make_tabs() -> list[Tab]:
  """Helper to make the tabs for the tab group demo."""
  state = me.state(State)
  tabs = [
    Tab(label="Tab 1", icon="home", content=tab_1),
    Tab(label="Tab 2", content=tab_2),
    Tab(label="Tab 3", icon="tab", content=tab_3),
  ]
  for index, tab in enumerate(tabs):
    tab.selected = state.selected_tab_index == index
    tab.disabled = index in state.disabled_tab_indexes
  return tabs


@me.component
def tab_1():
  me.text("Tab 1")


@me.component
def tab_2():
  me.text("Tab 2")


@me.component
def tab_3():
  me.text("Tab 3")


def on_tab_click(e: me.ClickEvent):
  """Click handler that handles updating the tabs when clicked."""
  state = me.state(State)

  _, tab_index = e.key.split("-")
  tab_index = int(tab_index)

  if tab_index == state.selected_tab_index:
    return
  if tab_index in state.disabled_tab_indexes:
    return

  state.selected_tab_index = int(tab_index)


@me.component
def tab_group(tabs: list[Tab], on_tab_click: Callable):
  """Generates the tab group component

  Args:
    tabs: Metadata for rendering tabs for the tab group
    on_tab_click: Event to handle what happens when a tab header is clicked
  """
  tab_header(tabs, on_tab_click)
  tab_content(tabs)


@me.component
def tab_header(tabs: list[Tab], on_tab_click: Callable):
  """Generates the header for the tab group."""
  with me.box(
    style=me.Style(
      display="flex",
      width="100%",
      border=me.Border(
        bottom=me.BorderSide(
          width=1, style="solid", color=me.theme_var("outline-variant")
        )
      ),
    )
  ):
    for index, tab in enumerate(tabs):
      with me.box(
        key=f"tab-{index}",
        on_click=on_tab_click,
        style=make_tab_style(tab.selected, tab.disabled),
      ):
        if tab.icon:
          me.icon(tab.icon)
        me.text(tab.label)


@me.component
def tab_content(tabs: list[Tab]):
  """Component for rendering the content of the selected tab."""
  for tab in tabs:
    if tab.selected:
      with me.box():
        tab.content()


def make_tab_style(selected: bool, disabled: bool) -> me.Style:
  """Makes the styles for the tab based on selected/disabled state."""
  style = make_default_tab_style()
  if disabled:
    style.color = me.theme_var("outline")
    style.cursor = "default"
  elif selected:
    style.background = me.theme_var("surface-container")
    style.border = me.Border(
      bottom=me.BorderSide(
        width=2, style="solid", color=me.theme_var("primary")
      )
    )
    style.cursor = "default"
  return style


def make_default_tab_style():
  """Basic styles shared by different tab state (selected, disabled, default)."""
  return me.Style(
    align_items="center",
    color=me.theme_var("on-surface"),
    display="flex",
    cursor="pointer",
    flex_grow=1,
    justify_content="center",
    line_height=1,
    font_size=14,
    font_weight="medium",
    padding=me.Padding.all(16),
    text_align="center",
    gap=5,
  )
