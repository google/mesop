from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./firebase_auth_component.js")
def firebase_auth_component(on_auth_changed: Callable[[mel.WebEvent], Any]):
  return mel.insert_web_component(
    name="firebase-auth-component",
    events={
      "authChanged": on_auth_changed,
    },
  )
