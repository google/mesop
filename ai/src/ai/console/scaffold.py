import mesop as me


@me.stateclass
class State:
  sidenav_menu_open: bool


def toggle_menu_button(e: me.ClickEvent):
  s = me.state(State)
  s.sidenav_menu_open = not s.sidenav_menu_open


def is_mobile():
  return me.viewport_size().width < 640


@me.content_component
def page_scaffold(current_path: str = "", title: str = "Mesop AI Console"):
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
        sidenav(current_path)
    else:
      sidenav(current_path)
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container-low"),
        display="flex",
        flex_direction="column",
        flex_grow=1,
      )
    ):
      header(title)
      with me.box(
        style=me.Style(
          background=me.theme_var("background"),
          flex_grow=1,
          padding=me.Padding(
            left=16,
            right=16,
            top=16,
          ),
          border_radius=16,
          overflow_y="auto",
          display="flex",
          flex_direction="column",
        )
      ):
        me.slot()


def toggle_theme(e: me.ClickEvent):
  if me.theme_brightness() == "light":
    me.set_theme_mode("dark")
  else:
    me.set_theme_mode("light")


def header(title: str):
  with me.box(
    style=me.Style(
      height=64,
      width="100%",
      padding=me.Padding.all(16),
      display="flex",
      align_items="center",
    ),
  ):
    me.text(
      title,
      style=me.Style(
        color=me.theme_var("on-background"),
        font_size=22,
        font_weight=500,
        letter_spacing="0.8px",
        padding=me.Padding(left=36) if is_mobile() else None,
      ),
    )

    with me.content_button(
      type="icon",
      style=me.Style(position="absolute", right=4, top=8),
      on_click=toggle_theme,
    ):
      me.icon("light_mode" if me.theme_brightness() == "dark" else "dark_mode")


def sidenav(current_path: str):
  with me.box(
    style=me.Style(
      width=240,
      min_width=240,
      max_width=240,
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
        gap=12,
      ),
    ):
      nav_link("Home", icon="home", path="/", current_path=current_path)
      nav_link("Evals", icon="labs", path="/evals", current_path=current_path)
      nav_link(
        "Producers",
        icon="precision_manufacturing",
        path="/producers",
        current_path=current_path,
      )
      nav_link(
        "Models", icon="model", path="/models", current_path=current_path
      )
      me.text(
        "Prompts",
        style=me.Style(
          font_weight=500, font_size=16, margin=me.Margin(top=4, left=4)
        ),
      )
      nav_link(
        "Prompt Contexts",
        icon="notebook",
        path="/prompt-contexts",
        current_path=current_path,
      )
      nav_link(
        "Prompt Fragments",
        icon="description",
        path="/prompt-fragments",
        current_path=current_path,
      )
      me.text(
        "Examples",
        style=me.Style(
          font_weight=500, font_size=16, margin=me.Margin(top=4, left=4)
        ),
      )
      nav_link(
        "Expected Examples",
        icon="labs",
        path="/expected-examples",
        current_path=current_path,
      )
      nav_link(
        "Golden Examples",
        icon="school",
        path="/golden-examples",
        current_path=current_path,
      )


def nav_link(
  label: str, icon: str, path: str, current_path: str, nested: bool = False
):
  with me.box(
    style=me.Style(
      cursor="pointer",
      margin=me.Margin(left=32) if nested else None,
      padding=me.Padding.all(12),
      border_radius=12,
      display="flex",
      align_items="center",
      gap=12,
      background=me.theme_var("secondary-container")
      if path == current_path
      else None,
      font_weight=500,
      font_size=16,
    ),
    key=path,
    on_click=lambda e: me.navigate(e.key),
  ):
    me.icon(icon)
    me.text(label)
