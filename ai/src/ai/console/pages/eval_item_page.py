import base64

import requests

import mesop as me
from ai.console.scaffold import page_scaffold
from ai.offline_common.eval import (
  SANDBOX_URL,
  get_eval_example,
)


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")
  state = me.state(State)
  example = get_eval_example(
    me.query_params["eval-id"], me.query_params["example-id"]
  )
  code = example.outputs[0].output.output_code or ""
  result = requests.post(
    SANDBOX_URL + "/exec",
    data={"code": base64.b64encode(code.encode("utf-8"))},
  )
  if result.status_code == 200:
    url_path = result.content.decode("utf-8")
    state.loaded_url = SANDBOX_URL + url_path
    state.error = ""
  else:
    state.error = result.content.decode("utf-8")


@me.stateclass
class State:
  loaded_url: str
  error: str


@me.page(title="Mesop AI Console - Eval", path="/eval-item", on_load=on_load)
def eval_item_page():
  state = me.state(State)
  example = get_eval_example(
    me.query_params["eval-id"], me.query_params["example-id"]
  )
  with page_scaffold(current_path="/eval", title="Eval"):
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="80px 1fr",
        gap=8,
        justify_items="start",
        margin=me.Margin(bottom=8),
      )
    ):
      with me.box(
        style=me.Style(
          display="grid",
          grid_template_columns="repeat(2, calc(calc(100vw - 310px)/2))",
          gap=16,
          align_items="start",
        )
      ):
        # Header
        me.text("Result", style=me.Style(font_weight="bold"))
        me.text("Preview", style=me.Style(font_weight="bold"))

        # Body
        with me.box(
          style=me.Style(
            display="flex",
            flex_direction="column",
            gap=8,
            height="calc(100vh - 160px)",
            overflow_y="auto",
          )
        ):
          me.text("ID", style=me.Style(font_weight="bold"))
          me.text(example.expected.id)

          me.text("Results", style=me.Style(font_weight="bold"))
          for result in example.outputs[0].expect_results:
            with me.box(
              style=me.Style(display="flex", flex_direction="row", gap=8)
            ):
              me.text(result.name)
              me.text(str(result.score))

            me.text(
              result.message,
              style=me.Style(font_family="monospace", white_space="pre"),
            )

          me.text("Output code")
          me.markdown(
            "```\n" + (example.outputs[0].output.output_code or "") + "\n```",
            style=me.Style(font_size=14),
          )
          me.divider()
          me.text("Raw output (diff)")
          raw_output = example.outputs[0].output.raw_output or ""
          prefix = "" if raw_output.startswith("```") else "```\n"
          suffix = "" if raw_output.endswith("```") else "\n```"
          me.markdown(
            prefix + raw_output + suffix,
            style=me.Style(font_size=14),
          )
          me.divider()
          me.text("Input code")
          me.markdown(
            "```\n" + (example.expected.input.input_code or "") + "\n```",
            style=me.Style(font_size=14),
          )

        with me.box(
          style=me.Style(display="flex", flex_direction="column", gap=8)
        ):
          if state.error:
            me.text("Error")
            me.text(state.error)
          me.embed(
            src=state.loaded_url, style=me.Style(width="100%", height="80vh")
          )
