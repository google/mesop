import time

import mesop as me
import mesop.labs as mel


@me.page(path="/text_to_text", title="Text I/O Example")
def app():
  mel.text_to_text(
    upper_case_stream,
    title="Text I/O Example",
  )


def upper_case_stream(s: str):
  yield s.capitalize()
  time.sleep(0.5)
  yield "Done"
