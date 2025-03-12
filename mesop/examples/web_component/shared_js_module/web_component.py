import mesop as me


@me.web_component(path="./web_component.js")
def web_component():
  return me.insert_web_component(name="shared-js-module-component")
