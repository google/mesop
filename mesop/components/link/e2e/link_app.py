import mesop as me


@me.page(path="/components/link/e2e/link_app")
def app():
  me.link(label="Hello, world!")
