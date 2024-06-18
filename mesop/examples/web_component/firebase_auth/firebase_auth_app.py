import mesop as me
from mesop.examples.web_component.firebase_auth.firebase_auth_component import (
  firebase_auth_component,
)


@me.page(
  path="/web_component/firebase_auth/firebase_auth_app",
  stylesheets=[
    "https://www.gstatic.com/firebasejs/ui/6.1.0/firebase-ui-auth.css"
  ],
)
def page():
  me.text("Loaded")
  firebase_auth_component()
