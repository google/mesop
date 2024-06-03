import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/progress_spinner",
)
def app():
  me.progress_spinner()
