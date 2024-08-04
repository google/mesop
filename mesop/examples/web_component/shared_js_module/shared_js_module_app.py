import mesop as me
from mesop.examples.web_component.shared_js_module.web_component import (
  web_component,
)


@me.page(
  path="/web_component/shared_js_module/shared_js_module_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
  ),
)
def page():
  me.text("Loaded")
  web_component()
