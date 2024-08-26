import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/box",
)
def app():
  with me.box(style=me.Style(background="red", padding=me.Padding.all(16))):
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
        background="cyan",
        height=50,
        margin=me.Margin.symmetric(vertical=24, horizontal=12),
        border=me.Border.symmetric(
          horizontal=me.BorderSide(width=2, color="black", style="groove")
        ),
      )
    ):
      me.text(text="Example with left and right borders")
