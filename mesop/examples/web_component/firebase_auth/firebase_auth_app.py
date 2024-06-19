import firebase_admin
from firebase_admin import auth

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.firebase_auth.firebase_auth_component import (
  firebase_auth_component,
)

# Avoid re-initializing firebase app (useful for avoiding warning message because of hot reloads).
if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
  default_app = firebase_admin.initialize_app()


@me.page(
  path="/web_component/firebase_auth/firebase_auth_app",
  stylesheets=[
    "https://www.gstatic.com/firebasejs/ui/6.1.0/firebase-ui-auth.css"
  ],
  # Loosen the security policy so the firebase JS libraries work.
  security_policy=me.SecurityPolicy(
    dangerously_disable_trusted_types=True,
    allowed_connect_srcs=["*.googleapis.com"],
    allowed_script_srcs=["*.google.com"],
  ),
)
def page():
  email = me.state(State).email
  if email:
    me.text("Signed in email: " + email)
  else:
    me.text("Not signed in")
  firebase_auth_component(on_auth_changed=on_auth_changed)


@me.stateclass
class State:
  email: str


def on_auth_changed(e: mel.WebEvent):
  print("AUTH", e.value)
  firebaseAuthToken = e.value
  if not firebaseAuthToken:
    me.state(State).email = ""
    return

  decoded_token = auth.verify_id_token(firebaseAuthToken)
  if decoded_token["email"] != "allowlisted.user@gmail.com":
    raise me.MesopUserException("Invalid user: " + decoded_token["email"])
  me.state(State).email = decoded_token["email"]
