import mesop as me


@me.page(
  path="/testing/csp_trusted_types",
  title="CSP trusted types",
  security_policy=me.SecurityPolicy(
    allowed_trusted_types=["ttpolicy1", "ttpolicy2"],
  ),
)
def page():
  me.text("CSP trusted types")
