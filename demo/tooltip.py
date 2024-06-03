import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/tooltip",
)
def app():
  with me.tooltip(message="Tooltip message"):
    me.text(text="Hello, World")
