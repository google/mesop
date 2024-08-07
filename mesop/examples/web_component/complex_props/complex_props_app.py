import mesop as me
from mesop.examples.web_component.complex_props.web_component import (
  web_component,
)


@me.page(
  path="/web_component/complex_props/complex_props_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
  ),
)
def page():
  me.text("Loaded")
  web_component(
    array=["element1", "element2"],
    object={
      "key1": "value1",
      "key2": "value2",
    },
  )
