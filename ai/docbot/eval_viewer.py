import itertools
import os
import sys
import urllib.parse
from dataclasses import dataclass, field

import mesop as me
import mesop.labs as mel

# Get the directory from the environment variable
EVAL_DIR = os.environ.get("EVAL_DIR")

if EVAL_DIR:
  print(f"Directory set to: {EVAL_DIR}")
else:
  print(
    "No directory specified. Exiting! Set the EVAL_DIR environment variable."
  )
  sys.exit(1)

EVAL_DIR_2 = os.environ.get("EVAL_DIR_2")

if EVAL_DIR_2:
  print(f"Eval directory 2 set to: {EVAL_DIR_2}")


@dataclass
class Item:
  query: str = ""
  input: str = ""
  output: str = ""


@dataclass
class EvalGroup:
  items: list[Item] = field(default_factory=list)


@me.stateclass
class State:
  directories: list[str]
  group_1: EvalGroup
  group_2: EvalGroup


def load_eval_dir(eval_dir: str):
  # Read all directories from args.dir
  directories = [
    d for d in os.listdir(eval_dir) if os.path.isdir(os.path.join(eval_dir, d))
  ]
  items: list[Item] = []
  for dir in directories:
    input_path = os.path.join(eval_dir, dir, "input.txt")
    output_path = os.path.join(eval_dir, dir, "output.txt")

    with open(input_path) as f:
      input_content = f.read()
    with open(output_path) as f:
      output_content = f.read()

    item = Item(
      input=input_content,
      output=output_content,
      query=urllib.parse.unquote(dir),
    )
    items.append(item)
  return items


def on_load(e: me.LoadEvent):
  state = me.state(State)
  assert EVAL_DIR
  state.group_1.items = load_eval_dir(EVAL_DIR)
  if EVAL_DIR_2:
    state.group_2.items = load_eval_dir(EVAL_DIR_2)
    print("state.group_2.items", state.group_2.items)

  # Store the directories in the state for later use
  # me.state(State).directories = directories


@me.page(
  on_load=on_load,
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
  ),
)
def index():
  state = me.state(State)
  with scrollable():
    with me.box(
      style=me.Style(
        margin=me.Margin.symmetric(horizontal="auto", vertical=24),
        # background="white",
        padding=me.Padding.symmetric(horizontal=16),
      )
    ):
      me.text("Eval viewer", type="headline-3")
      me.text(f"Group 1: {len(state.group_1.items)} items")
      me.text(f"Group 2: {len(state.group_2.items)} items")

      # Zip group_1 and group_2 items
      zipped_items = list(
        itertools.zip_longest(
          state.group_1.items, state.group_2.items, fillvalue=None
        )
      )
      with me.box(
        style=me.Style(
          display="grid",
          grid_template_columns="160px 300px 1fr 300px 1fr"
          if state.group_2.items
          else "160px 1fr 1fr",
          gap=16,
        )
      ):
        # Header
        me.text("Query", style=me.Style(font_weight=500))
        me.text("Input (1)", style=me.Style(font_weight=500))
        me.text("Output (1)", style=me.Style(font_weight=500))
        if state.group_2.items:
          me.text("Input (2)", style=me.Style(font_weight=500))
          me.text("Output (2)", style=me.Style(font_weight=500))
        # Body
        for item_1, item_2 in zipped_items:
          if item_1:
            me.text(item_1.query, style=me.Style(font_weight=500))
            me.markdown(
              item_1.input, style=me.Style(overflow_y="auto", max_height=400)
            )
            me.text(item_1.output)

          if item_2:
            me.markdown(
              item_2.input, style=me.Style(overflow_y="auto", max_height=400)
            )
            me.text(item_2.output)


@mel.web_component(path="./scrollable.js")
def scrollable(
  *,
  key: str | None = None,
):
  return mel.insert_web_component(
    name="scrollable-component",
    key=key,
  )
