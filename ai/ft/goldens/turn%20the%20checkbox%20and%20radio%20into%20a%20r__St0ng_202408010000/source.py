import mesop as me


@me.page(path="/checkbox_and_radio")
def page():
  me.text("Checkbox and radio")
  me.radio(
    options=[
      me.RadioOption(label="Option 1"),
      me.RadioOption(label="Option 2"),
    ]
  )
  me.checkbox("Checkbox 1")
  me.checkbox("Checkbox 2")
  me.text("More text")
