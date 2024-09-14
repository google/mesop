# Disable import sort ordering due to the hack needed
# to ensure local imports.
# ruff: noqa: E402

import base64
import inspect
import os
import sys
from dataclasses import dataclass
from typing import Literal

import mesop as me

# Append the current directory to sys.path to ensure local imports work
# This is required so mesop/examples/__init__.py can import the modules
# imported below.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
  sys.path.append(current_dir)

import glob

import audio as audio
import autocomplete as autocomplete
import badge as badge
import basic_animation as basic_animation
import box as box
import button as button
import chat as chat
import chat_inputs as chat_inputs
import checkbox as checkbox
import code_demo as code_demo  # cannot call it code due to python library naming conflict
import density as density
import dialog as dialog
import divider as divider
import embed as embed
import fancy_chat as fancy_chat
import feedback as feedback
import form_billing as form_billing
import form_profile as form_profile
import grid_table as grid_table
import headers as headers
import html_demo as html_demo
import icon as icon
import image as image
import input as input
import link as link
import llm_playground as llm_playground
import llm_rewriter as llm_rewriter
import markdown_demo as markdown_demo  # cannot call it markdown due to python library naming conflict
import markdown_editor as markdown_editor
import plot as plot
import progress_bar as progress_bar
import progress_spinner as progress_spinner
import radio as radio
import select_demo as select_demo  # cannot call it select due to python library naming conflict
import sidenav as sidenav
import slide_toggle as slide_toggle
import slider as slider
import snackbar as snackbar
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
      Example(name="fancy_chat"),
      Example(name="llm_rewriter"),
      Example(name="llm_playground"),
      Example(name="markdown_editor"),
    ],
  ),
  Section(
    name="Patterns",
    examples=[
      Example(name="dialog"),
      Example(name="grid_table"),
      Example(name="headers"),
      Example(name="snackbar"),
      Example(name="chat_inputs"),
      Example(name="form_billing"),
      Example(name="form_profile"),
    ],
  ),
  Section(
    name="Features",
    examples=[
      Example(name="density"),
    ],
  ),
  Section(
    name="Misc",
    examples=[
      Example(name="basic_animation"),
      Example(name="feedback"),
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
      Example(name="code_demo"),
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
      Example(name="autocomplete"),
      Example(name="button"),
      Example(name="checkbox"),
      Example(name="input"),
      Example(name="textarea"),
      Example(name="radio"),
      Example(name="select_demo"),
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
    name="Web",
    examples=[
      Example(name="embed"),
      Example(name="html_demo"),
      Example(name="link"),
    ],
  ),
  Section(
    name="Others",
    examples=[
      Example(name="plot"),
    ],
  ),
]

ALL_SECTIONS = FIRST_SECTIONS + COMPONENTS_SECTIONS

BORDER_SIDE = me.BorderSide(
  style="solid",
  width=1,
  color="#dcdcdc",
)


@me.stateclass
class State:
  current_demo: str
  panel_fullscreen: Literal["preview", "editor", None] = None


screenshots: dict[str, str] = {}


def load_home_page(e: me.LoadEvent):
  if me.state(ThemeState).dark_mode:
    me.set_theme_mode("dark")
  else:
    me.set_theme_mode("system")
  yield
  screenshot_dir = os.path.join(current_dir, "screenshots")
  screenshot_files = glob.glob(os.path.join(screenshot_dir, "*.webp"))

  for screenshot_file in screenshot_files:
    image_name = os.path.basename(screenshot_file).split(".")[0]
    with open(screenshot_file, "rb") as image_file:
      encoded_string = base64.b64encode(image_file.read()).decode()
      screenshots[image_name] = "data:image/webp;base64," + encoded_string

  yield


@me.page(
  title="Mesop Demos",
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  on_load=load_home_page,
)
def main_page():
  header()
  with me.box(
    style=me.Style(
      background=me.theme_var("background"),
      flex_grow=1,
      display="flex",
    )
  ):
    if is_desktop():
      side_menu()
    with me.box(
      style=me.Style(
        width="calc(100% - 150px)" if is_desktop() else "100%",
        display="flex",
        gap=24,
        flex_direction="column",
        padding=me.Padding.all(24),
        overflow_y="auto",
      )
    ):
      with me.box(
        style=me.Style(
          height="calc(100vh - 120px)",
        )
      ):
        for section in ALL_SECTIONS:
          with me.box(style=me.Style(margin=me.Margin(bottom=28))):
            me.text(
              section.name,
              style=me.Style(
                font_weight=500,
                font_size=20,
                margin=me.Margin(
                  bottom=16,
                ),
              ),
            )
            with me.box(
              style=me.Style(
                display="flex",
                flex_direction="row",
                flex_wrap="wrap",
                gap=28,
              )
            ):
              for example in section.examples:
                example_card(example.name)


def navigate_example_card(e: me.ClickEvent):
  me.navigate("/embed/" + e.key)


def example_card(name: str):
  with me.box(
    key=name,
    on_click=navigate_example_card,
    style=me.Style(
      border=me.Border.all(
        me.BorderSide(
          width=1,
          color="rgb(220, 220, 220)",
          style="solid",
        )
      ),
      box_shadow="rgba(0, 0, 0, 0.2) 0px 3px 1px -2px, rgba(0, 0, 0, 0.14) 0px 2px 2px, rgba(0, 0, 0, 0.12) 0px 1px 5px",
      cursor="pointer",
      width="min(100%, 150px)",
      border_radius=12,
      background=me.theme_var("background"),
    ),
  ):
    image_url = screenshots.get(name, "")
    me.box(
      style=me.Style(
        background=f'url("{image_url}") center / cover',
        height=112,
        width=150,
      )
    )
    me.text(
      format_example_name(name),
      style=me.Style(
        font_weight=500,
        font_size=18,
        padding=me.Padding.all(12),
        border=me.Border(
          top=me.BorderSide(
            width=1,
            style="solid",
            color="rgb(220, 220, 220)",
          )
        ),
      ),
    )


def on_load_embed(e: me.LoadEvent):
  if me.state(ThemeState).dark_mode:
    me.set_theme_mode("dark")
  else:
    me.set_theme_mode("system")
  if not is_desktop():
    me.state(State).panel_fullscreen = "preview"


def create_main_fn(example: Example):
  @me.page(
    on_load=on_load_embed,
    title="Mesop Demos",
    path="/embed/" + example.name,
    security_policy=me.SecurityPolicy(
      allowed_iframe_parents=["https://google.github.io"]
    ),
  )
  def main():
    with me.box(
      style=me.Style(
        height="100%",
        display="flex",
        flex_direction="column",
        background=me.theme_var("background"),
      )
    ):
      header(demo_name=example.name)
      body(example.name)

  return main


for section in FIRST_SECTIONS + COMPONENTS_SECTIONS:
  for example in section.examples:
    create_main_fn(example)


def body(current_demo: str):
  state = me.state(State)
  with me.box(
    style=me.Style(
      flex_grow=1,
      display="flex",
    )
  ):
    if is_desktop():
      side_menu()
    src = "/" + current_demo
    with me.box(
      style=me.Style(
        width="calc(100% - 150px)" if is_desktop() else "100%",
        display="grid",
        grid_template_columns="1fr 1fr"
        if state.panel_fullscreen is None
        else "1fr",
      )
    ):
      if state.panel_fullscreen != "editor":
        demo_ui(src)
      if state.panel_fullscreen != "preview":
        demo_code(inspect.getsource(get_module(current_demo)))


def demo_ui(src: str):
  state = me.state(State)
  with me.box(
    style=me.Style(flex_grow=1),
  ):
    with me.box(
      style=me.Style(
        display="flex",
        justify_content="space-between",
        align_items="center",
        border=me.Border(bottom=BORDER_SIDE),
      )
    ):
      me.text(
        "Preview",
        style=me.Style(
          font_weight=500,
          padding=me.Padding.all(14),
        ),
      )
      if is_desktop():
        with me.tooltip(
          position="above",
          message="Minimize"
          if state.panel_fullscreen == "preview"
          else "Maximize",
        ):
          with me.content_button(type="icon", on_click=toggle_fullscreen):
            me.icon(
              "close_fullscreen"
              if state.panel_fullscreen == "preview"
              else "fullscreen"
            )
      else:
        swap_button()
    me.embed(
      src=src,
      style=me.Style(
        border=me.Border.all(me.BorderSide(width=0)),
        border_radius=2,
        height="calc(100vh - 106px)",
        width="100%",
      ),
    )


def swap_button():
  state = me.state(State)
  with me.tooltip(
    position="above",
    message="Swap for code"
    if state.panel_fullscreen == "preview"
    else "Swap for preview",
  ):
    with me.content_button(type="icon", on_click=swap_fullscreen):
      me.icon("swap_horiz")


def swap_fullscreen(e: me.ClickEvent):
  state = me.state(State)
  if state.panel_fullscreen == "preview":
    state.panel_fullscreen = "editor"
  else:
    state.panel_fullscreen = "preview"


def toggle_fullscreen(e: me.ClickEvent):
  state = me.state(State)
  if state.panel_fullscreen == "preview":
    state.panel_fullscreen = None
  else:
    state.panel_fullscreen = "preview"


def demo_code(code_arg: str):
  with me.box(
    style=me.Style(
      flex_grow=1,
      overflow_x="hidden",
      overflow_y="hidden",
      border=me.Border(
        left=BORDER_SIDE,
      ),
      background=me.theme_var("surface-container-low"),
    )
  ):
    with me.box(
      style=me.Style(
        display="flex",
        justify_content="space-between",
        align_items="center",
        border=me.Border(bottom=BORDER_SIDE),
        background=me.theme_var("background"),
      )
    ):
      me.text(
        "Code",
        style=me.Style(
          font_weight=500,
          padding=me.Padding.all(14),
        ),
      )
      if not is_desktop():
        swap_button()
    # Use four backticks for code fence to avoid conflicts with backticks being used
    # within the displayed code.
    me.markdown(
      f"""````python
{code_arg}
````
              """,
      style=me.Style(
        border=me.Border(
          right=BORDER_SIDE,
        ),
        font_size=13,
        height="calc(100vh - 106px)",
        overflow_y="auto",
        width="100%",
      ),
    )


def header(demo_name: str | None = None):
  with me.box(
    style=me.Style(
      border=me.Border(
        bottom=me.BorderSide(
          style="solid",
          width=1,
          color="#dcdcdc",
        )
      ),
      overflow_x="clip",
    )
  ):
    with me.box(
      style=me.Style(
        display="flex",
        align_items="end",
        justify_content="space-between",
        margin=me.Margin(left=12, right=12, bottom=12),
        font_size=24,
      )
    ):
      with me.box(style=me.Style(display="flex")):
        with me.box(
          style=me.Style(display="flex", cursor="pointer"),
          on_click=navigate_home,
        ):
          me.text(
            "Mesop", style=me.Style(font_weight=700, margin=me.Margin(right=8))
          )
          me.text("Demos ")
        if demo_name:
          me.text(
            "— " + format_example_name(demo_name),
            style=me.Style(white_space="nowrap", text_overflow="ellipsis"),
          )
      with me.box(style=me.Style(display="flex", align_items="baseline")):
        with me.box(
          style=me.Style(
            display="flex",
            align_items="baseline",
          ),
        ):
          me.link(
            text="google/mesop",
            url="https://github.com/google/mesop/",
            open_in_new_tab=True,
            style=me.Style(
              font_size=18,
              color=me.theme_var("primary"),
              text_decoration="none",
              margin=me.Margin(left=8, right=4, bottom=-16, top=-16),
            ),
          )
        me.text(
          "v" + me.__version__,
          style=me.Style(font_size=18, margin=me.Margin(left=16)),
        )
        with me.content_button(
          type="icon",
          style=me.Style(left=8, right=4, top=4),
          on_click=toggle_theme,
        ):
          me.icon(
            "light_mode" if me.theme_brightness() == "dark" else "dark_mode"
          )


@me.stateclass
class ThemeState:
  dark_mode: bool


def toggle_theme(e: me.ClickEvent):
  if me.theme_brightness() == "light":
    me.set_theme_mode("dark")
    me.state(ThemeState).dark_mode = True
  else:
    me.set_theme_mode("light")
    me.state(ThemeState).dark_mode = False


def navigate_home(e: me.ClickEvent):
  me.navigate("/")


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
      path = f"/embed/{example.name}"
      with me.box(
        style=me.Style(color=me.theme_var("primary"), cursor="pointer"),
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


def is_desktop():
  return me.viewport_size().width > 760
