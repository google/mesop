import mesop as me


@me.page(path="/components/box/e2e/box_app")
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
