import mesop.labs as mel


@mel.web_component(path="./web_component.js")
def web_component():
  return mel.insert_web_component(name="shared-js-module-component")
