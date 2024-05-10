import mesop as me


@me.page(path="/divider")
def app():
  me.text(text="before")
  me.divider()
  me.text(text="after")
