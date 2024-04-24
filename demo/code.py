import inspect

import mesop as me


@me.page(path="/code")
def code():
  me.text("Defaults to Python")
  me.code("a = 123")

  me.text("Can set to other languages")
  me.code("<div class='a'>foo</div>", language="html")

  me.text("Bigger code block")
  me.code(inspect.getsource(me))
