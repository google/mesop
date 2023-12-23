import mesop as me
from mesop.examples.shared.navmenu import scaffold


@me.page(path="/")
def index():
  with scaffold(url="/"):
    body()


def body():
  with me.box(style="""background: white; padding: 16px;"""):
    me.markdown(
      """
# Welcome
This is an example multi-page Mesop application which features common use cases.
"""
    )
