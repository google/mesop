import mesop as me


@me.page(path="/dynamic_values")
def app():
  me.text()
  hi = "hi"
  me.text(f"This field contains a variable {hi}")
