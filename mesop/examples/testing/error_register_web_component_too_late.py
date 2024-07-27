import mesop as me
import mesop.labs as mel


@me.page(path="/testing/error_register_web_component_too_late")
def page():
  me.text("error_register_web_component_too_late")

  @mel.web_component(path="./fake_module.js")
  def web_component():
    pass
