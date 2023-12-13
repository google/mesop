import mesop as me


@me.page(path="/components/box/e2e/box_app")
def app():
  with me.box(background_color="pink"):
    me.text(text="hi1")
    me.text(text="hi2")
