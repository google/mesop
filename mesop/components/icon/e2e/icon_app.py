import mesop as me


@me.page(path="/components/icon/e2e/icon_app")
def app():
  me.text(text="Hello, world!")
  me.icon(icon="home", style=me.Style(color="orange"))
