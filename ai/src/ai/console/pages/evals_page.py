import mesop as me
from ai.common.eval import eval_store as store
from ai.console.scaffold import page_scaffold


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(title="Mesop AI Console - Evals", path="/evals", on_load=on_load)
def evals_page():
  with page_scaffold(current_path="/evals", title="Evals"):
    evals = store.get_all()
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="repeat(2, 1fr)",
        gap=16,
        align_items="center",
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Name", style=me.Style(font_weight="bold"))
      # Body
      for eval in evals:
        me.button(
          eval.id,
          on_click=lambda e: me.navigate("/eval", query_params={"id": e.key}),
          key=eval.id,
          style=me.Style(font_size=16),
        )
        me.button(
          eval.producer_id,
          on_click=lambda e: me.navigate(
            "/producers/edit", query_params={"id": e.key}
          ),
          key=eval.producer_id,
          style=me.Style(font_size=16),
        )

    with me.box(style=me.Style(padding=me.Padding(top=32))):
      me.button(
        "Create eval",
        on_click=lambda e: me.navigate("/evals/add"),
        type="flat",
        color="accent",
      )
