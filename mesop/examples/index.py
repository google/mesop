# Use this file to import all examples
# Use import alias so Ruff doesn't complain about unused imports
import mesop as me
from mesop.examples import error as error
from mesop.examples import generator as generator
from mesop.examples import hello_world as hello_world
from mesop.examples import nested as nested
from mesop.examples import playground as playground

# Do not import error_state_missing_init_prop because it cause all examples to fail.
from mesop.examples import simple as simple
from mesop.examples import simple_button as simple_button


@me.page()
def index():
  with me.box(
    style="""
  height: 100%;
  background: white;
  """
  ):
    with me.box(
      style="""
      position: fixed;
    width: 96px;
    border-right: 1px solid #f6f5f6;
    height: 100%;
    """
    ):
      menu_item(label="Home", icon="home", url="/")
      menu_item(label="Settings", icon="settings", url="/playground")
    body()


def body():
  with me.box(style="margin-left: 108px; background: white;"):
    for _ in range(100):
      me.text("Hello world")


def menu_item(label: str, icon: str, url: str):
  def on_click(event: me.ClickEvent):
    me.navigate(url)

  with me.box(
    style="""
  padding: 16px;
  text-align: center;
  """
  ):
    with me.box(style="margin-bottom: 8px;"):
      with me.button(variant="icon", on_click=on_click):
        with me.box(
          style="""
        display: flex;
        flex-direction: column;
        align-items: center;
        """
        ):
          me.icon(icon=icon, style="color: oklch(0.5484 0.023 304.99)")
          me.text(
            label,
            style="""
            color: oklch(0.5484 0.023 304.99);
            font-weight: 500;
            font-size: 16px;
            """,
          )
