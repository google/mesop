import mesop as me


@me.page(path="/grid")
def app():
  with me.box(style=me.Style(display="grid", grid_template_columns="1fr 1fr")):
    me.text("hi1")
    me.text("hi2")
    me.text("hi3")
    me.text("hi4")
