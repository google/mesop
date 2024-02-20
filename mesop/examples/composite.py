import mesop as me


@me.page(path="/composite")
def app():
  with composite():
    me.text("hi")


@me.content_component
def composite():
  with me.box(
    style=me.Style(
      background="pink",
      padding=me.Padding(top=15, right=15, bottom=15, left=15),
    )
  ):
    with me.box(
      style=me.Style(
        background="orange",
        padding=me.Padding(top=15, right=15, bottom=15, left=15),
      )
    ):
      with me.box(
        style=me.Style(
          background="green",
          padding=me.Padding(top=15, right=15, bottom=15, left=15),
        )
      ):
        me.slot()
        me.text("hello")
