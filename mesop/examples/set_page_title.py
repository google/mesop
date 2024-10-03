import mesop as me


def on_blur(e: me.InputBlurEvent):
  me.set_page_title(e.value)


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/set_page_title",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.input(label="Page title", on_blur=on_blur)
