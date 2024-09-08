import mesop as me


@me.stateclass
class State:
  sidenav_menu_open: bool


def toggle_menu_button(e: me.ClickEvent):
  s = me.state(State)
  s.sidenav_menu_open = not s.sidenav_menu_open


def is_mobile():
  return me.viewport_size().width < 640


@me.page(
  title="Responsive layout",
  path="/responsive_layout",
)
def page():
  with me.box(style=me.Style(display="flex", height="100%")):
    if is_mobile():
      with me.content_button(
        type="icon",
        style=me.Style(top=6, left=8, position="absolute", z_index=9),
        on_click=toggle_menu_button,
      ):
        me.icon("menu")
      with me.sidenav(
        opened=me.state(State).sidenav_menu_open,
        style=me.Style(
          background=me.theme_var("surface-container-low"),
        ),
      ):
        sidenav()
    else:
      sidenav()
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container-low"),
        display="flex",
        flex_direction="column",
        flex_grow=1,
      )
    ):
      header()
      body()


def header():
  with me.box(
    style=me.Style(
      height=120,
      width="100%",
      padding=me.Padding.all(16),
      display="flex",
      align_items="center",
    ),
  ):
    me.text(
      "Title",
      style=me.Style(
        color=me.theme_var("on-background"),
        font_size=22,
        font_weight=500,
        letter_spacing="0.8px",
        padding=me.Padding(left=36) if is_mobile() else None,
      ),
    )


def body():
  with me.box(
    style=me.Style(
      background=me.theme_var("background"),
      flex_grow=1,
      padding=me.Padding(
        left=32,
        right=32,
        top=32,
        bottom=64,
      ),
      border_radius=16,
      overflow_y="auto",
    )
  ):
    me.text("Body")


def sidenav():
  with me.box(
    style=me.Style(
      width=216,
      height="100%",
      background=me.theme_var("surface-container-low"),
      padding=me.Padding.all(16),
    )
  ):
    with me.box(
      style=me.Style(
        padding=me.Padding(top=24),
        display="flex",
        flex_direction="column",
        gap=8,
      ),
    ):
      me.text(
        "Sidenav",
        style=me.Style(
          font_weight=500,
          letter_spacing="0.4px",
          padding=me.Padding(left=12),
        ),
      )
