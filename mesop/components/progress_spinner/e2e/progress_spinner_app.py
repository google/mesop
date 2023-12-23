import mesop as me


@me.page(path="/components/progress_spinner/e2e/progress_spinner_app")
def app():
  me.text(text="Two usages of spinners")
  me.spinner()  # spinner is the same as progress_spinner
  me.progress_spinner(diameter=40, stroke_width=4)
