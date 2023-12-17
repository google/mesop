import mesop as me


@me.page(path="/components/progress_bar/e2e/progress_bar_app")
def app():
  me.text(text="Hello, world!")
  me.progress_bar(mode="indeterminate")
