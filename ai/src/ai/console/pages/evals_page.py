import mesop as me
from ai.console.scaffold import page_scaffold
from ai.console.utils import calculate_eval_score
from ai.offline_common.eval import eval_store as store


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(title="Mesop AI Console - Evals", path="/evals", on_load=on_load)
def evals_page():
  with page_scaffold(current_path="/evals", title="Evals"):
    evals = store.get_all()
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.button(
        "Create eval",
        on_click=lambda e: me.navigate("/evals/add"),
        type="flat",
        color="accent",
      )

    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="1fr 1fr 96px 96px 96px",
        gap=16,
        align_items="center",
        padding=me.Padding(bottom=12),
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Name", style=me.Style(font_weight="bold"))
      me.text("State", style=me.Style(font_weight="bold"))
      me.text("Score", style=me.Style(font_weight="bold"))
      me.text("Examples Succeeded / Run", style=me.Style(font_weight="bold"))
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="1fr 1fr 96px 96px 96px",
        gap=16,
        align_items="center",
        height="100%",
        overflow_y="auto",
      )
    ):
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
        me.text(eval.state)
        if eval.eval_outcome:
          me.text(calculate_eval_score(eval.eval_outcome))
          me.text(
            f"{eval.eval_outcome.examples_succeeded} / {eval.eval_outcome.examples_run}"
          )
        else:
          me.text("N/A")
          me.text("N/A")
