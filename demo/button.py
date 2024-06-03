import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/button",
)
def main():
  me.text("Button types:", style=me.Style(margin=me.Margin(bottom=12)))
  with me.box(style=me.Style(display="flex", flex_direction="row", gap=12)):
    me.button("default")
    me.button("raised", type="raised")
    me.button("flat", type="flat")
    me.button("stroked", type="stroked")

  me.text("Button colors:", style=me.Style(margin=me.Margin(bottom=12)))
  with me.box(style=me.Style(display="flex", flex_direction="row", gap=12)):
    me.button("default", type="flat")
    me.button("primary", color="primary", type="flat")
    me.button("secondary", color="accent", type="flat")
    me.button("warn", color="warn", type="flat")
