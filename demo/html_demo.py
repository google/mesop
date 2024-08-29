import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/html_demo",
)
def app():
  me.text("Sanitized HTML")
  me.html(
    """
Custom HTML
<a href="https://google.github.io/mesop/" target="_blank">mesop</a>
""",
    mode="sanitized",
  )
  with me.box(style=me.Style(margin=me.Margin.symmetric(vertical=24))):
    me.divider()
  me.text("Sandboxed HTML")
  me.html(
    "hi<script>document.body.innerHTML = 'iamsandboxed'; </script>",
    mode="sandboxed",
  )
