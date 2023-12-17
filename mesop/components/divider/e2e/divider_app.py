import mesop as me


@me.page(path="/components/divider/e2e/divider_app")
def app():
  me.text(text="before")
  me.divider()
  me.text(text="after")
