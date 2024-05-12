# Disable import sort ordering due to the hack needed
# to ensure local imports.
# ruff: noqa: E402

import inspect
import os
import sys
from dataclasses import dataclass

import mesop as me

# Append the current directory to sys.path to ensure local imports work
# This is required so mesop/examples/__init__.py can import the modules
# imported below.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
  sys.path.append(current_dir)


import code as code
import select as select

import audio as audio
import badge as badge
import box as box
import button as button
import chat as chat
import checkbox as checkbox
import divider as divider
import embed as embed
import icon as icon
import image as image
import input as input
import llm_playground as llm_playground
import llm_rewriter as llm_rewriter
import markdown_demo as markdown_demo  # cannot call it markdown due to python library naming conflict
import plot as plot
import progress_bar as progress_bar
import progress_spinner as progress_spinner
import radio as radio
import sidenav as sidenav
import slide_toggle as slide_toggle
import slider as slider
import table as table
import text as text
import text_to_image as text_to_image
import text_to_text as text_to_text
import textarea as textarea
import tooltip as tooltip
import uploader as uploader
import video as video


@dataclass
class Example:
  # module_name (should also be the path name)
  name: str


@dataclass
class Section:
  name: str
  examples: list[Example]


FIRST_SECTIONS = [
  Section(
    name="Quick start",
    examples=[
      Example(name="chat"),
      Example(name="text_to_image"),
      Example(name="text_to_text"),
    ],
  ),
  Section(
    name="Use cases",
    examples=[
      Example(name="llm_rewriter"),
      Example(name="llm_playground"),
    ],
  ),
]

COMPONENTS_SECTIONS = [
  Section(
    name="Layout",
    examples=[
      Example(name="box"),
      Example(name="sidenav"),
    ],
  ),
  Section(
    name="Text",
    examples=[
      Example(name="text"),
      Example(name="markdown_demo"),
      Example(name="code"),
    ],
  ),
  Section(
    name="Media",
    examples=[
      Example(name="image"),
      Example(name="audio"),
      Example(name="video"),
    ],
  ),
  Section(
    name="Form",
    examples=[
      Example(name="button"),
      Example(name="checkbox"),
      Example(name="input"),
      Example(name="textarea"),
      Example(name="radio"),
      Example(name="select"),
      Example(name="slide_toggle"),
      Example(name="slider"),
      Example(name="uploader"),
    ],
  ),
  Section(
    name="Visual",
    examples=[
      Example(name="badge"),
      Example(name="divider"),
      Example(name="icon"),
      Example(name="progress_bar"),
      Example(name="progress_spinner"),
      Example(name="table"),
      Example(name="tooltip"),
    ],
  ),
  Section(
    name="Advanced",
    examples=[
      Example(name="embed"),
      Example(name="plot"),
    ],
  ),
]

BORDER_SIDE = me.BorderSide(
  style="solid",
  width=1,
  color="#dcdcdc",
)


@me.stateclass
class State:
  current_demo: str


def create_main_fn(example: Example):
  @me.page(
    title="Mesop Demos",
    path="/" if example.name == "chat" else "/embed/" + example.name,
  )
  def main():
    with me.box(
      style=me.Style(
        height="100%",
        display="flex",
        flex_direction="column",
        background="#fff",
      )
    ):
      header(demo_name=example.name)
      body(example.name)

  return main


for section in FIRST_SECTIONS + COMPONENTS_SECTIONS:
  for example in section.examples:
    create_main_fn(example)


def body(current_demo: str):
  with me.box(
    style=me.Style(
      flex_grow=1,
      display="flex",
    )
  ):
    side_menu()
    src = "/" + current_demo
    with me.box(
      style=me.Style(
        width="calc(100% - 160px)",
        display="grid",
        grid_template_columns="1fr 1fr",
      )
    ):
      demo_ui(src)
      demo_code(inspect.getsource(get_module(current_demo)))


def demo_ui(src: str):
  with me.box(
    style=me.Style(flex_grow=1),
  ):
    box_header("Preview")
    me.embed(
      src=src,
      style=me.Style(
        border=me.Border.all(me.BorderSide(width=0)),
        border_radius=2,
        height="calc(100vh - 120px)",
        width="100%",
      ),
    )


def box_header(header_text: str):
  me.text(
    header_text,
    style=me.Style(
      font_weight=500,
      padding=me.Padding.all(8),
      border=me.Border(
        bottom=BORDER_SIDE,
        right=BORDER_SIDE,
      ),
    ),
  )


def demo_code(code_arg: str):
  with me.box(
    style=me.Style(
      flex_grow=1,
      overflow_x="hidden",
      overflow_y="hidden",
      border=me.Border(
        left=BORDER_SIDE,
      ),
    )
  ):
    box_header("Code")
    me.markdown(
      f"""```
{code_arg}
```
              """,
      style=me.Style(
        border=me.Border(
          right=BORDER_SIDE,
        ),
        font_size=13,
        padding=me.Padding.all(12),
        height="calc(100vh - 120px)",
        overflow_y="auto",
        width="100%",
      ),
    )


def header(demo_name: str):
  with me.box(
    style=me.Style(
      border=me.Border(
        bottom=me.BorderSide(
          style="solid",
          width=1,
          color="#dcdcdc",
        )
      ),
    )
  ):
    with me.box(
      style=me.Style(
        display="flex",
        align_items="end",
        justify_content="space-between",
        margin=me.Margin.all(12),
        font_size=24,
      )
    ):
      with me.box(style=me.Style(display="flex")):
        me.text(
          "Mesop", style=me.Style(font_weight=700, margin=me.Margin(right=8))
        )
        me.text("Demos — " + format_example_name(demo_name))
      me.text(
        "v" + me.__version__,
        style=me.Style(font_size=18, margin=me.Margin(left=8)),
      )


def side_menu():
  with me.box(
    style=me.Style(
      padding=me.Padding.all(12),
      width=150,
      flex_grow=0,
      line_height="1.5",
      border=me.Border(right=BORDER_SIDE),
      overflow_x="hidden",
      height="calc(100vh - 60px)",
      overflow_y="auto",
    )
  ):
    for section in FIRST_SECTIONS:
      nav_section(section)
    with me.box(
      style=me.Style(
        margin=me.Margin.symmetric(
          horizontal=-16,
          vertical=16,
        ),
      )
    ):
      me.divider()
    me.text(
      "Components",
      style=me.Style(
        letter_spacing="0.5px",
        margin=me.Margin(bottom=6),
      ),
    )
    for section in COMPONENTS_SECTIONS:
      nav_section(section)


def nav_section(section: Section):
  with me.box(style=me.Style(margin=me.Margin(bottom=12))):
    me.text(section.name, style=me.Style(font_weight=700))
    for example in section.examples:
      example_name = format_example_name(example.name)
      path = f"/embed/{example.name}" if example.name != "chat" else "/"
      with me.box(
        style=me.Style(color="#0B57D0", cursor="pointer"),
        on_click=set_demo,
        key=path,
      ):
        me.text(example_name)


def set_demo(e: me.ClickEvent):
  me.navigate(e.key)


def format_example_name(name: str):
  return (
    (" ".join(name.split("_")))
    .capitalize()
    .replace("Llm", "LLM")
    .replace(" demo", "")
  )


def get_module(module_name: str):
  if module_name in globals():
    return globals()[module_name]
  raise me.MesopDeveloperException(f"Module {module_name} not supported")
