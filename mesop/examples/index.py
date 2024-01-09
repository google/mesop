import mesop as me
from mesop.examples.shared.navmenu import scaffold


@me.page(path="/")
def index():
  with scaffold(url="/"):
    body()


def body():
  with me.box(
    style=me.Style(
      background="white",
      padding=me.Padding(top=16, bottom=16, left=16, right=16),
    )
  ):
    me.markdown(
      """
# Welcome
This is an example multi-page Mesop application which features common use cases.
"""
    )
