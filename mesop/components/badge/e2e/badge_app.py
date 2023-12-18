import mesop as me


@me.page(path="/components/badge/e2e/badge_app")
def app():
  with me.box(
    style="""
    display: block;
    padding: 16px;
              height: 50px;
              width: 30px;
              background: pink;
  """
  ):
    with me.badge(content="1"):
      me.text(text="some badge")
