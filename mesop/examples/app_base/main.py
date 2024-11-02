import os

import mesop as me


@me.page(path="/examples/app_base")
def page():
  me.text(
    "Testing: MESOP_APP_BASE_PATH="
    + os.getenv("MESOP_APP_BASE_PATH", "<not set>")
  )
