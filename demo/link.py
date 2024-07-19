import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/link",
)
def link():
  me.link(text="Open in same tab", url="https://google.github.io/mesop/")
  me.link(
    text="Open in new tab",
    open_in_new_tab=True,
    url="https://google.github.io/mesop/",
  )
  me.link(
    text="Styled link",
    url="https://google.github.io/mesop/",
    style=me.Style(color="black", text_decoration="none"),
  )
