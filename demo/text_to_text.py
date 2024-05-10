import mesop as me
import mesop.labs as mel


@me.page(path="/text_to_text", title="Text to Text Example")
def app():
  mel.text_io(
    upper_case_stream,
    title="Text to Text Example",
  )


def upper_case_stream(s: str):
  return "Echo: " + s
