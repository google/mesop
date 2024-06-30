import mesop as me


@me.page(path="/components/html/e2e/html_app")
def app():
  s = me.state(State)

  me.text("Sanitized HTML")
  me.html(
    """
Custom HTML
<a href="https://google.github.io/mesop/" target="_blank">mesoplink</a>
""",
    mode="sanitized",
  )
  with me.box(style=me.Style(margin=me.Margin.symmetric(vertical=24))):
    me.divider()
  me.text("Sandboxed HTML")
  me.button("Increment sandboxed HTML", on_click=increment_sandboxed_html)
  me.html(
    f"iamsandboxed-{s.counter}<script>console.log('iamsandboxed-{s.counter}'); </script>",
    mode="sandboxed",
  )


@me.stateclass
class State:
  counter: int


def increment_sandboxed_html(e: me.ClickEvent):
  s = me.state(State)
  s.counter += 1
