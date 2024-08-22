import mesop as me


@me.stateclass
class State:
  clicks: int


def button_click(event: me.ClickEvent):
  state = me.state(State)
  state.clicks += 1


@me.page(path="/counter")
def main():
  state = me.state(State)

  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      align_items="center",
      padding=me.Padding.all(24),
      background=me.theme_var("surface"),
      border_radius=8,
      box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
      min_width=300,
      max_width=600,
      margin=me.Margin.symmetric(horizontal="auto"),
    )
  ):
    me.text(
      "Counter", type="headline-4", style=me.Style(margin=me.Margin(bottom=16))
    )
    me.text(
      f"Clicks: {state.clicks}",
      type="subtitle-1",
      style=me.Style(margin=me.Margin(bottom=16)),
    )

    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="column",
        align_items="center",
        gap=24,
        margin=me.Margin(bottom=32),
      )
    ):
      with me.box(
        style=me.Style(
          display="flex", flex_direction="row", align_items="center", gap=12
        )
      ):
        me.button(
          "Increment",
          on_click=button_click,
          type="flat",
          style=me.Style(
            border_radius=4,
            padding=me.Padding.symmetric(horizontal=16, vertical=8),
            color=me.theme_var("primary"),
          ),
        )
        with me.box(
          style=me.Style(
            background=me.theme_var("surface"),
            border_radius=4,
            padding=me.Padding.all(8),
          )
        ):
          me.text(
            "New Button",
            style=me.Style(
              color=me.theme_var("on-surface"),
              padding=me.Padding.symmetric(horizontal=16, vertical=8),
            ),
          )
