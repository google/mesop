import mesop as me
import mesop.labs as mel


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/text_to_text",
  title="Text to Text Example",
)
def app():
  mel.text_to_text(
    upper_case_stream,
    title="Text to Text Example",
  )


def upper_case_stream(s: str):
  return "Echo: " + s
