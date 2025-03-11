import mesop as me


@me.page(
  path="/testing/csp_font_srcs",
  title="CSP font_srcs",
  security_policy=me.SecurityPolicy(
    allowed_font_srcs=["fontsrc1", "fontsrc2"],
  ),
)
def page():
  me.text("CSP font srcs")
