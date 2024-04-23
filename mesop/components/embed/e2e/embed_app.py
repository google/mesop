import mesop as me


@me.page(path="/components/embed/e2e/embed_app")
def app():
  state = me.state(State)
  me.button("Switch src url", on_click=switch_src_url)
  me.embed(
    src=state.src_url if state.src_url else "https://google.github.io/mesop/",
    style=me.Style(width="100%", height="100%"),
  )


@me.stateclass
class State:
  src_url: str


def switch_src_url(e: me.ClickEvent):
  state = me.state(State)
  state.src_url = "https://google.github.io/mesop/internal/publishing/"
