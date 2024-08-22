import mesop as me


@me.stateclass
class State:
  sidebar_open: bool


def toggle_sidebar(e: me.ClickEvent):
  state = me.state(State)
  state.sidebar_open = not state.sidebar_open


@me.page()
def main_page():
  state = me.state(State)

  with me.box(
    style=me.Style(display="flex", flex_direction="column", min_height="100vh")
  ):
    # Header
    with me.box(
      style=me.Style(
        background=me.theme_var("primary"),
        padding=me.Padding.all(16),
        display="flex",
        align_items="center",
      )
    ):
      with me.content_button(
        type="icon",
        on_click=toggle_sidebar,
        style=me.Style(
          color="white",
          border=me.Border.all(me.BorderSide(width=1, color="white")),
        ),
      ):
        me.icon("menu")
      me.text("My App", style=me.Style(color="white", font_size=28))

    # Body (with sidebar)
    with me.box(style=me.Style(display="flex", flex_grow=1)):
      # Sidebar
      if state.sidebar_open:
        with me.box(
          style=me.Style(
            width=300,
            background=me.theme_var("surface"),
            padding=me.Padding.all(24),
            border=me.Border(
              right=me.BorderSide(width=1, color=me.theme_var("outline"))
            ),
          )
        ):
          me.text("Sidebar", type="headline-5", style=me.Style(margin=me.Margin(bottom=16)))
          with me.box(style=me.Style(display="flex", flex_direction="column", gap=12)):
            for item in ["Menu Item 1", "Menu Item 2", "Menu Item 3"]:
              me.text(item, type="body-1", style=me.Style(padding=me.Padding.symmetric(vertical=8)))

      # Main content
      with me.box(style=me.Style(flex_grow=1, padding=me.Padding.all(16))):
        me.text("Main Content", type="headline-5")
        me.text("This is the main content area of the application.")

    # Footer
    with me.box(
      style=me.Style(
        background=me.theme_var("surface"),
        padding=me.Padding.all(16),
        text_align="center",
        border=me.Border(
          top=me.BorderSide(width=1, color=me.theme_var("outline"))
        ),
      )
    ):
      me.text("© 2024 My App. All rights reserved.", type="caption")
