import mesop as me


@me.page(path="/components/input/e2e/input_app")
def app():
  me.input(label="Hello, world!")
