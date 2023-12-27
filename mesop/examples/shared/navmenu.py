import mesop as me


def navmenu(url: str):
  with me.box(
    style="""
    background: white;
      position: fixed;
    width: 84px;
    border-right: 1px solid #f6f5f6;
    height: 100%;
    """
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
  is_active_border = "border-left: 3px solid black;" if is_active else ""
  with me.box(
    style=f"""
    {is_active_border}
  padding: 16px;
  text-align: center;
  """
  ):
    with me.box(style="margin-bottom: 8px;"):
      with me.button(type="icon", on_click=on_click, key=url):
        with me.box(
          style="""
        display: flex;
        flex-direction: column;
        align-items: center;
        """
        ):
          me.icon(icon=icon, style=f"color: {color}")
          me.text(
            label,
            style=f"""
            color: {color};
            font-weight: 500;
            font-size: 14px;
            """,
          )


@me.composite
def scaffold(url: str):
  with me.box(style="background: white; height: 100%"):
    navmenu(url=url)
    with me.box(style="padding-left: 84px; height: 100%"):
      me.slot()
