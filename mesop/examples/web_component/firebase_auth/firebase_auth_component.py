from typing import Any, Callable

import mesop as me


@me.web_component(path="./firebase_auth_component.js")
def firebase_auth_component(on_auth_changed: Callable[[me.WebEvent], Any]):
  return me.insert_web_component(
    name="firebase-auth-component",
    events={
      "authChanged": on_auth_changed,
    },
  )
