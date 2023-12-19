import mesop as me


@me.page(path="/composite")
def app():
  with composite():
    me.text("hi")


@me.composite
def composite():
  with me.box(style="background-color: pink; padding: 15px"):
    with me.box(style="background-color: orange; padding: 15px"):
      with me.box(style="background-color: green; padding: 15px"):
        me.slot()
        me.text("hello")
