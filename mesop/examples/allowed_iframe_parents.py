import mesop as me


@me.page(
  path="/allowed_iframe_parents",
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["google.com"],
  ),
)
def app():
  me.text("Test CSP")
