import mesop as me


@me.page(path="/components/text/e2e/text_app")
def text():
  me.text(text="H1: Hello, world!", type="headline-1")
