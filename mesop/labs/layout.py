import mesop as me


@me.component()
def columns(columns: int = 2):
  return me.box(style=me.Style(columns=columns))
