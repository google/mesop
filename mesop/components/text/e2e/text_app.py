import mesop as me


@me.page(path="/components/text/e2e/text_app")
def text():
  me.text(text="H1: Hello, world!", type=me.Typography.H1)
  me.text(text="H2: Hello, world!", type=me.Typography.H2)
  me.text(text="H3: Hello, world!", type=me.Typography.H3)
  me.text(text="H4: Hello, world!", type=me.Typography.H4)
  me.text(text="H5: Hello, world!", type=me.Typography.H5)
  me.text(text="H6: Hello, world!", type=me.Typography.H6)
  me.text(text="Subtitle1: Hello, world!", type=me.Typography.SUBTITLE1)
  me.text(text="Subtitle2: Hello, world!", type=me.Typography.SUBTITLE2)
  me.text(text="Body1: Hello, world!", type=me.Typography.BODY1)
  me.text(text="Body2: Hello, world!", type=me.Typography.BODY2)
  me.text(text="Caption: Hello, world!", type=me.Typography.CAPTION)
