import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  me.text(text="headline-1: Hello, world!", type="headline-1")
  me.text(text="headline-2: Hello, world!", type="headline-2")
  me.text(text="headline-3: Hello, world!", type="headline-3")
  me.text(text="headline-4: Hello, world!", type="headline-4")
  me.text(text="headline-5: Hello, world!", type="headline-5")
  me.text(text="headline-6: Hello, world!", type="headline-6")
  me.text(text="subtitle-1: Hello, world!", type="subtitle-1")
  me.text(text="subtitle-2: Hello, world!", type="subtitle-2")
  me.text(text="body-1: Hello, world!", type="body-1")
  me.text(text="body-2: Hello, world!", type="body-2")
  me.text(text="caption: Hello, world!", type="caption")
  me.text(text="button: Hello, world!", type="button")
