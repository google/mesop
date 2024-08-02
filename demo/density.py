import mesop as me


def select_density(e: me.SelectSelectionChangeEvent):
  me.set_theme_density(int(e.value))  # type: ignore


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/density",
)
def main():
  me.select(
    label="Density",
    options=[
      me.SelectOption(label="0 (least dense)", value="0"),
      me.SelectOption(label="-1", value="-1"),
      me.SelectOption(label="-2", value="-2"),
      me.SelectOption(label="-3", value="-3"),
      me.SelectOption(label="-4 (most dense)", value="-4"),
    ],
    on_selection_change=select_density,
  )
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
