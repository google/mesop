import time

import mesop as me
import mesop.labs as mel


@me.page(path="/text_io")
def app():
  mel.text_io(upper_case_stream)


def upper_case(s: str) -> str:
  time.sleep(0.5)
  return s.capitalize()


def upper_case_stream(s: str):
  yield s.capitalize()
  time.sleep(0.5)
  yield s.capitalize() + "foo"
  time.sleep(0.5)
  yield s.capitalize() + "foo" + "bar"
