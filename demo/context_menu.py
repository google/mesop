"""Simple context menu example"""

from pydantic import BaseModel

import mesop as me


class MenuItem(BaseModel):
  label: str


class Menu(BaseModel):
  items: list[MenuItem]


CONTEXT_MENU = Menu(
  items=[
    MenuItem(label="Item 1"),
    MenuItem(label="Item 2"),
    MenuItem(label="Item 3"),
  ]
)


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.stateclass
class State:
  menu_active: bool = False
  menu_pos_x: int = 0
  menu_pos_y: int = 0
  selected_menu_item: str


@me.page(
  path="/context_menu",
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=[
      "https://mesop-dev.github.io",
    ]
  ),
  stylesheets=["/static/context_menu.css"],
  on_load=on_load,
)
def app():
  state = me.state(State)

  context_menu(CONTEXT_MENU)

  with me.box(
    style=me.Style(margin=me.Margin.all(15), width="100%", height="100%"),
    on_right_click=on_right_click,
  ):
    me.text("Selected menu item: " + state.selected_menu_item)
    me.text("[Right click anywhere show a context menu]")


@me.component
def context_menu(menu: Menu):
  """Really simply context menu component."""
  state = me.state(State)
  with me.box(
    on_click=on_click_outside_menu,
    style=me.Style(
      background="rgba(0, 0, 0, 0)",
      # Use display block/none so that the event handler does not get removed.
      # If we use a conditional, this event handler will not be found when it bubbles up
      # on menu item click.
      display="block" if state.menu_active else "none",
      height="100%",
      overflow_x="auto",
      overflow_y="auto",
      position="fixed",
      width="100%",
      z_index=1000,
    ),
  ):
    with me.box(
      style=me.Style(
        position="absolute",
        top=state.menu_pos_y,
        left=state.menu_pos_x,
      )
    ):
      with me.box(
        style=me.Style(
          background=me.theme_var("surface-container-highest"),
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
          padding=me.Padding.symmetric(vertical=10),
          min_width=125,
          border_radius=10,
        )
      ):
        for item in menu.items:
          with me.box(
            key=item.label,
            classes="menu-item",
            style=me.Style(
              cursor="pointer",
              padding=me.Padding.symmetric(vertical=10, horizontal=15),
              font_weight="medium",
            ),
            on_click=on_click_menu_item,
          ):
            me.text(item.label)


def on_click_menu_item(e: me.ClickEvent):
  """Handles click events on context menu items"""
  state = me.state(State)
  state.selected_menu_item = e.key
  state.menu_active = False
  state.menu_pos_x = 0
  state.menu_pos_y = 0


def on_click_outside_menu(e: me.ClickEvent):
  """Handles clicking outside the context menu when it is open (i.e. closes the context menu)"""
  # Ensure the click is outside the context menu
  if not e.is_target:
    return
  state = me.state(State)
  state.selected_menu_item = ""
  state.menu_active = False
  state.menu_pos_x = 0
  state.menu_pos_y = 0


def on_right_click(e: me.RightClickEvent):
  """Handle right click event by opening custom context menu"""
  state = me.state(State)
  state.menu_active = True
  state.menu_pos_x = int(e.client_x)
  state.menu_pos_y = int(e.client_y)
