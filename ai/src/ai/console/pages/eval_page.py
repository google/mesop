import mesop as me
from ai.console.scaffold import page_scaffold
from ai.console.utils import calculate_eval_score
from ai.offline_common.eval import EvalRunner, get_eval_examples
from ai.offline_common.eval import eval_store as store


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


def run_eval(e: me.ClickEvent):
  eval = store.get(me.query_params["id"])
  EvalRunner(eval).run()


def delete_eval(e: me.ClickEvent):
  store.delete(me.query_params["id"])
  me.navigate("/evals")


@me.page(title="Mesop AI Console - Eval", path="/eval", on_load=on_load)
def eval_page():
  eval = store.get(me.query_params["id"])
  examples = get_eval_examples(eval.id)
  with page_scaffold(current_path="/eval", title="Eval"):
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="80px 1fr",
        gap=8,
        justify_items="start",
      )
    ):
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text(eval.id)
      me.text("State", style=me.Style(font_weight="bold"))
      me.text(eval.state)
      me.text("Examples", style=me.Style(font_weight="bold"))
      me.text(str(len(examples)))
      if eval.eval_outcome:
        me.text("Score", style=me.Style(font_weight="bold"))
        with me.tooltip(
          message=f"Score: {eval.eval_outcome.score} / Max score: {eval.eval_outcome.examples_run * 3}"
        ):
          me.text(calculate_eval_score(eval.eval_outcome))
    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="row",
        justify_content="space-between",
        padding=me.Padding.symmetric(vertical=16),
      )
    ):
      if eval.state == "pending":
        me.button(
          "Run eval",
          on_click=run_eval,
          type="flat",
          color="accent",
        )

      me.button(
        "Delete eval",
        on_click=delete_eval,
        type="flat",
        color="warn",
      )

    if eval.state == "complete":
      with me.box(
        style=me.Style(
          display="grid",
          grid_template_columns="220px 300px 32px 48px 1fr",
          gap=16,
          align_items="center",
        )
      ):
        # Header
        me.text("ID", style=me.Style(font_weight="bold"))
        me.text("Prompt", style=me.Style(font_weight="bold"))
        me.text("Secs", style=me.Style(font_weight="bold"))
        me.text("Tokens", style=me.Style(font_weight="bold"))
        me.text("Expect results", style=me.Style(font_weight="bold"))
        # Body
        for example in examples:
          # use a link because back navigation drops the query params
          me.link(
            text=example.expected.id,
            style=me.Style(
              font_size=16,
              text_decoration="none",
              color=me.theme_var("primary"),
            ),
            url=f"/eval-item?example-id={example.expected.id}&eval-id={eval.id}",
          )
          me.text(example.expected.input.prompt)
          me.text(f"{example.outputs[0].time_spent_secs:.1f}")
          me.text(str(example.outputs[0].tokens))
          with me.box(
            style=me.Style(display="flex", flex_direction="row", gap=12)
          ):
            for result in example.outputs[0].expect_results:
              with me.tooltip(message=result.message or ""[-300:-120]):
                with me.box(
                  style=me.Style(
                    display="flex",
                    flex_direction="column",
                    gap=8,
                    background=me.theme_var("error-container")
                    if result.score == 0
                    else None,
                    padding=me.Padding.all(4),
                    border_radius=8,
                  )
                ):
                  me.text(result.name[:5], style=me.Style(font_weight="bold"))
                  me.text(str(result.score))
