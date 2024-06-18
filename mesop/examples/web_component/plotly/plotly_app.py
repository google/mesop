import mesop as me
from mesop.examples.web_component.plotly.plotly_component import (
  plotly_component,
)


@me.page(
  path="/web_component/plotly/plotly_app",
  # CAUTION: this disables an important web security feature and
  # should not be used for most mesop apps.
  #
  # Disabling trusted types because plotly uses DomParser#parseFromString
  # which violates TrustedHTML assignment.
  security_policy=me.SecurityPolicy(dangerously_disable_trusted_types=True),
)
def page():
  plotly_component()
