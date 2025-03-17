import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/progress_bar",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("Default progress bar", type="headline-5")
    me.progress_bar()
