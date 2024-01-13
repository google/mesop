import mesop as me


def app():
  with me.box():
    me.text("sibling")
  me.divider()
