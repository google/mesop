import mesop as me


def app():
  me.radio(
    options=[
      me.RadioOption(value="1", label="l1"),
      me.RadioOption(value="2", label="l2"),me.RadioOption()
    ]
  )
