import inspect

import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/code_demo",
)
def code_demo():
  with me.box(
    style=me.Style(
      padding=me.Padding.all(15),
      background=me.theme_var("surface-container-lowest"),
    )
  ):
    me.text("Defaults to Python")
    me.code("a = 123")

    me.text("Can set to other languages")
    me.code("<div class='a'>foo</div>", language="html")

    me.text("Bigger code block")
    me.code(inspect.getsource(me))
