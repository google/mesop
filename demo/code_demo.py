import inspect

import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/code_demo",
)
def code_demo():
  me.text("Defaults to Python")
  me.code("a = 123")

  me.text("Can set to other languages")
  me.code("<div class='a'>foo</div>", language="html")

  me.text("Bigger code block")
  me.code(inspect.getsource(me))
