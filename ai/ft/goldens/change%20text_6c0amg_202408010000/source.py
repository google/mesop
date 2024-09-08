import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  me.text(text="headline-1: Hello, world!", type="headline-1", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-2: Hello, world!", type="headline-2", style=me.Style(color=me.theme_var("primary")))
  me.text(text="Welcome to Mesop!", type="headline-4", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-4: Hello, world!", type="headline-4", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-5: Hello, world!", type="headline-5", style=me.Style(color=me.theme_var("primary")))
  me.text(text="headline-6: Hello, world!", type="headline-6", style=me.Style(color=me.theme_var("primary")))
  me.text(text="subtitle-1: Hello, world!", type="subtitle-1", style=me.Style(color=me.theme_var("primary")))
  me.text(text="subtitle-2: Hello, world!", type="subtitle-2", style=me.Style(color=me.theme_var("primary")))
  me.text(text="body-1: Hello, world!", type="body-1", style=me.Style(color=me.theme_var("on-surface"), font_size=18))
  me.text(text="body-2: Hello, world!", type="body-2", style=me.Style(color=me.theme_var("on-surface")))
  me.text(text="caption: Hello, world!", type="caption", style=me.Style(color=me.theme_var("on-surface-variant")))
  me.text(text="button: Hello, world!", type="button", style=me.Style(color=me.theme_var("primary")))
  wrap_button()

  with me.box(style=me.Style(padding=me.Padding.all(24), background=me.theme_var("surface"))):
    me.text("inside box1", style=me.Style(color=me.theme_var("on-surface")))
    me.text("inside box2", style=me.Style(color=me.theme_var("on-surface")))


@me.component
def wrap_button():
  me.button("button")
