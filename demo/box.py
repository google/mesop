import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/box",
)
def app():
  border_style = ["dashed", "dotted", "double", "groove", "inset", "outset"]
  with me.box(style=me.Style(background="red", padding=me.Padding.all(16))):
    for style in border_style:
      with me.box(
        style=me.Style(
          background="green",
          height=50,
          margin=me.Margin.symmetric(vertical=24, horizontal=12),
          border=me.Border.symmetric(
            horizontal=me.BorderSide(width=2, color="pink", style=style),
            vertical=me.BorderSide(width=2, color="orange", style=style),
          ),
        )
      ):
        me.text(text="hi1")
        me.text(text="hi2")
