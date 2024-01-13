import mesop as me


@me.page(path="/components/progress_spinner/e2e/progress_spinner_app")
def app():
  me.progress_spinner()  # default spinner
  me.progress_spinner(diameter=40, stroke_width=4)
  me.text("Two usages of spinners")
