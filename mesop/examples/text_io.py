import time

import mesop as me
import mesop.labs as mel


@me.page(path="/text_io", title="Text I/O Example")
def app():
  mel.text_io(
    upper_case_stream,
    title="Text I/O Example",
  )


def upper_case_stream(s: str):
  yield s.capitalize()
  time.sleep(0.5)
  yield s.capitalize() + "foo"
  time.sleep(0.5)
  yield s.capitalize() + "foo" + "bar"


# For simpler transformations, you can directly
# return a string value like this:
# def upper_case(s: str) -> str:
#   time.sleep(0.5)
#   return s.capitalize()
