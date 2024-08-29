import base64
import json
import os
import urllib.parse
from typing import Any

import requests

import mesop as me

DEFAULT_URL = "http://localhost:8080"


@me.stateclass
class State:
  # Set by query params
  golden: bool
  model: str
  run_name: str

  # Others
  dirs: list[str]
  stats: dict[str, Any]

  selected_dir_path: str

  loaded_url: str
  show_error_dialog: bool
  error: str


GOLDENS_PATH = "../ft/goldens"
OUTPUTS_PATH = "../outputs"


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")
  state = me.state(State)
  if "golden" in me.query_params:
    state.golden = True
    file_path = GOLDENS_PATH
  else:
    state.model = me.query_params["model"]
    state.run_name = me.query_params["run_name"]
    file_path = get_file_path()
  stats_path = os.path.join(file_path, "stats.json")
  with open(stats_path) as f:
    state.stats = json.load(f)
  dirs = [
    d
    for d in os.listdir(file_path)
    if os.path.isdir(os.path.join(file_path, d))
  ]

  state.dirs = dirs


def get_file_path() -> str:
  state = me.state(State)
  return os.path.join(OUTPUTS_PATH, state.model, state.run_name)


@me.page(title="Viewer", on_load=on_load)
def main():
  state = me.state(State)
  with me.box(
    style=me.Style(
      padding=me.Padding.all(24),
      display="flex",
      flex_direction="column",
      height="100%",
    )
  ):
    with me.box(style=me.Style(display="flex", flex_direction="row", gap=16)):
      me.text(f"Viewing: {state.model}/{state.run_name}")
      me.text(f"Success: {state.stats['success_count']}")
      me.text(f"Error: {state.stats['error_count']}")

    me.box(style=me.Style(height=16))
    me.divider()
    me.box(style=me.Style(height=16))

    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="1fr 1fr" if state.selected_dir_path else "1fr",
        flex_grow=1,
        overflow_y="hidden",
      )
    ):
      grid()
      if state.selected_dir_path:
        with me.box(
          style=me.Style(
            display="flex",
            flex_direction="column",
            gap=16,
            overflow_y="hidden",
          )
        ):
          viewer()


def viewer():
  state = me.state(State)
  if state.show_error_dialog:
    me.text("ERR!")
    me.text(str(state.error))
  if state.selected_dir_path:
    me.embed(src=state.loaded_url, style=me.Style(width="100%", height="80vh"))
  else:
    me.text("No directory selected")


def grid():
  state = me.state(State)
  with me.box(
    style=me.Style(
      display="grid",
      grid_template_columns="300px 140px 1fr 1fr",
      align_items="center",
      gap=16,
      overflow_y="auto",
    )
  ):
    me.text("Prompt", style=me.Style(font_weight="bold"))
    me.text("Source File", style=me.Style(font_weight="bold"))
    me.text("Error/run")
    me.text("Links")
    for dir in state.dirs:
      dir_row(dir)


def dir_row(dir: str):
  parsed_dir = urllib.parse.unquote(dir)
  parts = parsed_dir.split("__")
  if "golden" in me.query_params:
    source_path = os.path.join(GOLDENS_PATH, dir, "source.py")
    source_file = str(os.path.exists(source_path))
    with open(os.path.join(GOLDENS_PATH, dir, "prompt.txt")) as f:
      prompt = f.read()
    root_dir = GOLDENS_PATH

  else:
    prompt = parts[0]
    source_file = parts[1]
    root_dir = "./" + get_file_path()

  dir_path = os.path.join(root_dir, dir)

  error_file_path = os.path.join(root_dir, dir, "error.txt")
  has_error = os.path.exists(error_file_path)
  me.text(prompt)
  me.text(source_file)
  error_action_cell(
    has_error=has_error, error_file_path=error_file_path, dir_path=dir_path
  )
  diff_path = os.path.join(
    os.path.dirname(__file__), get_file_path(), dir, "diff.txt"
  )
  patched_path = os.path.join(
    os.path.dirname(__file__), get_file_path(), dir, "patched.py"
  )
  error_file_path = os.path.join(
    os.path.dirname(__file__), get_file_path(), dir, "error.txt"
  )
  with me.box(style=me.Style(display="flex", flex_direction="row", gap=0)):
    file_link(text="diff.txt", path=diff_path)
    file_link(text="patched.py", path=patched_path)
    if has_error:
      file_link(text="error.txt", path=error_file_path)


def file_link(*, text: str, path: str):
  me.link(
    text=text,
    url="/file?path=" + urllib.parse.quote(path),
    open_in_new_tab=True,
    style=me.Style(
      color=me.theme_var("primary"),
      text_decoration="none",
      padding=me.Padding(right=12),
    ),
  )


def navigate_to_file(e: me.ClickEvent):
  me.navigate("/file", query_params={"path": e.key})


@me.stateclass
class FileViewerState:
  contents: str


def on_load_file_viewer(e: me.LoadEvent):
  me.set_theme_mode("system")
  state = me.state(FileViewerState)
  with open(me.query_params["path"]) as f:
    state.contents = f.read()


@me.page(title="File Viewer", path="/file", on_load=on_load_file_viewer)
def file_viewer():
  state = me.state(FileViewerState)
  me.text(
    state.contents,
    style=me.Style(font_family="monospace", white_space="pre", font_size=14),
  )


def error_action_cell(*, has_error: bool, error_file_path: str, dir_path: str):
  with me.box(style=me.Style(display="flex", flex_direction="column", gap=0)):
    if has_error:
      with open(error_file_path) as f:
        error_text = f.read()
      me.text(
        error_text[:30],
        style=me.Style(
          font_size=12, font_family="monospace", white_space="break-spaces"
        ),
      )

    with me.content_button(
      type="icon", color="primary", on_click=click_row, key=dir_path
    ):
      me.icon(icon="play_arrow")


def click_row(e: me.ClickEvent):
  state = me.state(State)
  state.selected_dir_path = e.key
  with open(os.path.join(e.key, "patched.py")) as f:
    code = f.read()
  result = requests.post(
    DEFAULT_URL + "/exec",
    data={"code": base64.b64encode(code.encode("utf-8"))},
  )
  if result.status_code == 200:
    url_path = result.content.decode("utf-8")
    state.loaded_url = DEFAULT_URL + url_path
    state.show_error_dialog = False
    state.error = ""
  else:
    state.show_error_dialog = True
    state.error = result.content.decode("utf-8")
