import mesop as me
from ai.common.example import golden_example_store as store
from ai.console.scaffold import page_scaffold


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(path="/golden-examples", on_load=on_load)
def golden_examples_page():
  with page_scaffold(current_path="/golden-examples", title="golden Examples"):
    examples = store.get_all()
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.button(
        "Add golden Example",
        on_click=lambda e: me.navigate("/golden-examples/add"),
        type="flat",
        color="accent",
      )
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="repeat(4, 1fr)",
        gap=16,
        align_items="center",
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Prompt", style=me.Style(font_weight="bold"))
      me.text("Has input code", style=me.Style(font_weight="bold"))
      me.text("Has line # target", style=me.Style(font_weight="bold"))
      # Body
      for example in examples:
        me.button(
          example.id,
          on_click=lambda e: me.navigate(
            "/golden-examples/edit", query_params={"id": e.key}
          ),
          key=example.id,
          style=me.Style(font_size=16),
        )
        me.text(example.input.prompt)
        me.text(str(bool(example.input.input_code)))
        me.text(str(bool(example.input.line_number_target)))
