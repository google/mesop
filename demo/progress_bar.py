import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/progress_bar",
)
def app():
  me.text("Default progress bar")
  me.progress_bar()
