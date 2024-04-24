import mesop as me


@me.page(path="/progress_bar")
def app():
  me.text("Default progress bar")
  me.progress_bar()
