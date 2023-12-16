import mesop as me


@me.page(path="/components/input/e2e/input_app")
def app():
  me.text(text="Hello, world!")
  me.input(label="Basic input")
