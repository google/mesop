import mesop as me
import mesop.labs as mel


@me.page(
  path="/testing/text_to_text",
  title="Text to Text Example",
)
def app():
  mel.text_to_text(
    echo,
    title="Text to Text Example",
  )


def echo(s: str):
  return "Echo: " + s
