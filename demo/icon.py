import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/icon",
)
def app():
  me.text("home icon")
  me.icon(icon="home")
