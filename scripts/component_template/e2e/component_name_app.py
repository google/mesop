import mesop as me


@me.page(path="/components/component_name/e2e/component_name_app")
def app():
  me.component_name(label="Hello, world!")
