import mesop as me


def select_density(e: me.SelectSelectionChangeEvent):
  me.set_theme_density(int(e.value))  # type: ignore


@me.page(
  path="/testing/theme_density",
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
  me.button("button", type="flat")
