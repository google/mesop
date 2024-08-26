import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/box",
)
def app():
  with me.box(style=me.Style(background="red", padding=me.Padding.all(16))):
    # Card at the top
    with me.box(
      style=me.Style(
        background=me.theme_var("surface"),
        padding=me.Padding.all(16),
        margin=me.Margin(bottom=24),
        border=me.Border.all(me.BorderSide(width=1, color=me.theme_var("outline"))),
        border_radius=8,
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.05)",
      )
    ):
      me.text(
        text="Welcome to My App",
        style=me.Style(
          color=me.theme_var("on-surface"),
          font_size=24,
          font_weight=600,
          margin=me.Margin(bottom=8),
      )
      )
      me.text(
        text="This is a simple card component created for demonstration purposes.",
        style=me.Style(
          color=me.theme_var("on-surface-variant"),
          font_size=16,
          font_weight=400,
        )
      )
    with me.box(
      style=me.Style(
        background="green",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          horizontal=me.BorderSide(width=2, color="pink", style="solid"),
          vertical=me.BorderSide(width=2, color="orange", style="solid"),
        ),
      )
    ):
      me.text(text="hi1")
      me.text(text="hi2")

    with me.box(
      style=me.Style(
        background="blue",
        height=50,
        margin=me.Margin.all(16),
        border=me.Border.all(
          me.BorderSide(width=2, color="yellow", style="dotted")
        ),
        border_radius=10,
      )
    ):
      me.text(text="Example with all sides bordered")

    with me.box(
      style=me.Style(
        background="purple",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          vertical=me.BorderSide(width=4, color="white", style="double")
        ),
      )
    ):
      me.text(text="Example with top and bottom borders")

    with me.box(
      style=me.Style(
        display="flex",
        align_items="center",
        background=me.theme_var("surface"),
        height=60,
        margin=me.Margin.symmetric(vertical=16, horizontal=12),
        border=me.Border.all(me.BorderSide(width=1, color=me.theme_var("outline"))),
        border_radius=8,
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
      )
    ):
      me.icon(icon="border_left", style=me.Style(margin=me.Margin(right=8), color=me.theme_var("primary")))
      me.text(
        text="Example with left and right borders",
        style=me.Style(color=me.theme_var("on-surface"), font_size=16, font_weight=500)
      )
