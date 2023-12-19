# Use this file to import all examples
# Use import alias so Ruff doesn't complain about unused imports
import mesop as me
from mesop.examples import buttons as buttons
from mesop.examples import composite as composite
from mesop.examples import error as error
from mesop.examples import generator as generator
from mesop.examples import hello_world as hello_world
from mesop.examples import nested as nested
from mesop.examples import playground as playground

# Do not import error_state_missing_init_prop because it cause all examples to fail.
from mesop.examples import simple as simple
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
