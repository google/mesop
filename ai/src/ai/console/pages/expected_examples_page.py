import mesop as me
from ai.common.example import expected_example_store as store
from ai.console.scaffold import page_scaffold


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(path="/expected-examples", on_load=on_load)
def expected_examples_page():
  with page_scaffold(
    current_path="/expected-examples", title="Expected Examples"
  ):
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.button(
        "Add Expected Example",
        on_click=lambda e: me.navigate("/expected-examples/add"),
        type="flat",
        color="accent",
      )

    examples = store.get_all()
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="240px 1fr 140px 140px 48px 48px",
        gap=16,
        align_items="center",
        padding=me.Padding(bottom=12),
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Prompt", style=me.Style(font_weight="bold"))
      me.text("Created at", style=me.Style(font_weight="bold"))
      me.text("Updated at", style=me.Style(font_weight="bold"))
      me.text("Has input code", style=me.Style(font_weight="bold"))
      me.text("Has line # target", style=me.Style(font_weight="bold"))
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="240px 1fr 140px 140px 48px 48px",
        gap=16,
        align_items="center",
        overflow_y="auto",
        height="100%",
      )
    ):
      # Body
      for example in examples:
        me.button(
          example.id,
          on_click=lambda e: me.navigate(
            "/expected-examples/edit", query_params={"id": e.key}
          ),
          key=example.id,
          style=me.Style(font_size=16),
        )
        me.text(example.input.prompt)
        if example.created_at:
          me.text(example.created_at.strftime("%Y-%m-%d"))
        else:
          me.text("")
        if example.updated_at:
          me.text(example.updated_at.strftime("%Y-%m-%d"))
        else:
          me.text("")
        me.text(str(bool(example.input.input_code)))
        me.text(str(bool(example.input.line_number_target)))
