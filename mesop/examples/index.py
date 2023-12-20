# Use this file to import all examples
# Use import alias so Ruff doesn't complain about unused imports
import mesop as me
from mesop.examples import buttons as buttons
from mesop.examples import composite as composite
from mesop.examples import error as error
from mesop.examples import generator as generator
from mesop.examples import nested as nested
from mesop.examples import playground as playground
from mesop.examples import playground_critic as playground_critic
from mesop.examples import readme_app as readme_app

# Do not import error_state_missing_init_prop because it cause all examples to fail.
from mesop.examples import simple as simple
from mesop.examples.docs import counter as counter
from mesop.examples.docs import hello_world as hello_world
from mesop.examples.docs import loading as loading
from mesop.examples.docs import streaming as streaming
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
