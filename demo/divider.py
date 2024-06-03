import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/divider",
)
def app():
  me.text(text="before")
  me.divider()
  me.text(text="after")
