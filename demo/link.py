import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/link",
)
def link():
  with me.box(
    style=me.Style(
      margin=me.Margin.all(15), display="flex", flex_direction="column", gap=10
    )
  ):
    me.link(
      text="Open in same tab",
      url="https://google.github.io/mesop/",
      style=me.Style(color=me.theme_var("primary")),
    )
    me.link(
      text="Open in new tab",
      open_in_new_tab=True,
      url="https://google.github.io/mesop/",
      style=me.Style(color=me.theme_var("primary")),
    )
    me.link(
      text="Styled link",
      url="https://google.github.io/mesop/",
      style=me.Style(color=me.theme_var("tertiary"), text_decoration="none"),
    )
