import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/html_demo",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("Sanitized HTML", type="headline-5")
    me.html(
      """
  Custom HTML
  <a href="https://google.github.io/mesop/" target="_blank">mesop</a>
  """,
      mode="sanitized",
    )

    with me.box(style=me.Style(margin=me.Margin.symmetric(vertical=24))):
      me.divider()

    me.text("Sandboxed HTML", type="headline-5")
    me.html(
      "<style>body { color: #ff0000; }</style>hi<script>document.body.innerHTML = 'iamsandboxed'; </script>",
      mode="sandboxed",
    )
