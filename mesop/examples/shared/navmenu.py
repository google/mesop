import mesop as me


def navmenu(url: str):
  with me.box(
    style=me.Style(
      background="white",
      position="fixed",
      width=84,
      border=me.Border(
        right=me.BorderSide(width=1, style="solid", color="#f6f5f6")
      ),
      height="100%",
    )
  ):
    menu_item(label="Home", icon="home", url="/", current_url=url)
    menu_item(
      label="Playground", icon="ar_stickers", url="/playground", current_url=url
    )
    menu_item(
      label="Playground Critic",
      icon="ar_stickers",
      url="/playground-critic",
      current_url=url,
    )
    menu_item(label="Buttons", icon="gamepad", url="/buttons", current_url=url)


def menu_item(label: str, icon: str, url: str, current_url: str):
  def on_click(event: me.ClickEvent):
    me.navigate(event.key)

  is_active = url == current_url
  color = "black" if is_active else "oklch(0.5484 0.023 304.99)"

  with me.box(
    style=me.Style(
      padding=me.Padding(top=16, bottom=16, left=16, right=16),
      text_align="center",
      border=me.Border(
        left=me.BorderSide(width=3, style="solid", color="black")
      )
      if is_active
      else None,
    )
  ):
    with me.box(style=me.Style(margin=me.Margin(bottom=8))):
      with me.content_button(type="icon", on_click=on_click, key=url):
        with me.box(
          style=me.Style(
            display="flex", flex_direction="column", align_items="center"
          )
        ):
          me.icon(icon=icon, style=me.Style(color=color))
          me.text(
            label,
            style=me.Style(color=color, font_weight=500, font_size=14),
          )


@me.content_component
def scaffold(url: str):
  with me.box(style=me.Style(background="white", height="100%")):
    navmenu(url=url)
    with me.box(style=me.Style(padding=me.Padding(left=84), height="100%")):
      me.slot()
