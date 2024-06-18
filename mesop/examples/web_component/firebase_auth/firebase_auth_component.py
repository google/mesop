import mesop.labs as mel


@mel.web_component(path="./firebase_auth_component.js")
def firebase_auth_component():
  return mel.insert_web_component(name="firebase-auth-component")
