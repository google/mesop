import mesop as me


@me.page(path="/viewport_size")
def app():
  me.text(
    f"viewport_size width={me.viewport_size().width} height={me.viewport_size().height}"
  )

  if me.viewport_size().width > 640:
    width = round(me.viewport_size().width / 2)
  else:
    width = me.viewport_size().width

  me.box(
    style=me.Style(
      width=width,
      height=40,
      background="blue",
    )
  )

  # Example of adaptive design:
  if me.viewport_size().width > 640:
    with me.box(
      style=me.Style(
        width="100%",
        height=100,
        background="pink",
      )
    ):
      me.text("Only shown on large screens")
