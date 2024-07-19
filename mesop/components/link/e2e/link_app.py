import mesop as me


@me.page(path="/components/link/e2e/link_app")
def app():
  me.link(text="Open in same tab", url="https://google.com")
  me.link(
    text="Styled link: Google",
    url="https://google.com",
    style=me.Style(color="black", text_decoration="none"),
  )
  me.link(
    text="Open in new tab",
    open_in_new_tab=True,
    url="https://google.com",
  )
