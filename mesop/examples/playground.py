import mesop as me


@me.page()
def app():
  header()
  body()


def header():
  with me.box(
    style="""
    background: white;
  border-bottom: 1px solid #ececf1;
  padding: 12px;
  """
  ):
    me.text(
      "Playground",
      type=me.Typography.H5,
      style="""
    margin: 0;
    """,
    )


def body():
  with me.box(
    style="""

  """
  ):
    me.input(label="Input", type=me.Textarea(rows=10))
