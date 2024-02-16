import os
import random
from dataclasses import dataclass

import mesop as me


@dataclass
class Output:
  query: str
  version: str
  content: str


@me.stateclass
class State:
  query: str
  reveal: bool


def on_navigate(e: me.ClickEvent):
  s = me.state(State)
  s.query = e.key
  s.reveal = False
  me.navigate(f"/sxs/{s.query}")


output_dict: dict[str, list[Output]] = {}


def extract_data(version: str):
  directory_path = f"mesop/examples/sxs/data/{version}"
  for item in os.listdir(directory_path):
    full_path = os.path.join(directory_path, item)
    query = os.path.splitext(item)[0]

    if os.path.isfile(full_path):
      with open(full_path) as file:
        content = file.read()

        output = Output(query=query, content=content, version=version)

      if query in output_dict:
        output_dict[query].append(output)
      else:
        output_dict[query] = [output]


extract_data("gemini")
extract_data("gemini_advanced")

for key in output_dict:
  random.shuffle(output_dict[key])


@me.page(path="/sxs")
def all_app():
  with me.box(
    style=me.Style(
      margin=me.Margin(top=16, right=16, left=16, bottom=16),
      display="grid",
      gap="16px",
    )
  ):
    for key in sorted(output_dict.keys()):
      me.button(
        key, on_click=on_navigate, key=key, type="raised", color="primary"
      )


def reveal(e: me.ClickEvent):
  s = me.state(State)
  s.reveal = True


for key in output_dict:

  @me.page(path=f"/sxs/{key}")
  def app(fn_key: str = key):
    outputs = output_dict[fn_key]
    with me.box(
      style=me.Style(
        display="flex",
        height="80%",
        overflow_y="auto",
      )
    ):
      with me.box(
        style=me.Style(flex_basis="100%" if len(outputs) == 1 else "50%")
      ):
        output_ui(outputs[0])
      if len(outputs) > 1:
        with me.box(style=me.Style(flex_basis="50%")):
          output_ui(outputs[1])
    with me.box(
      style=me.Style(
        box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        height="20%",
        padding=me.Padding(
          top=16,
          left=16,
          right=16,
          bottom=16,
        ),
        background="#f0f4f8",
      )
    ):
      with me.box(
        style=me.Style(
          background="#fff",
          border_radius=12,
          padding=me.Padding(
            top=16,
            left=16,
            right=16,
            bottom=16,
          ),
        )
      ):
        me.text(
          "Select which one is better:",
          style=me.Style(font_weight=500),
        )
        with me.box(
          style=me.Style(
            padding=me.Padding(top=12, bottom=16),
            display="flex",
            width="400px",
            flex_direction="row",
            justify_content="space-around",
          )
        ):
          me.button(
            "Prefer left", type="raised", color="primary", on_click=reveal
          )
          me.box(style=me.Style(width=16))
          me.button("Neutral", type="raised", color="primary", on_click=reveal)
          me.box(style=me.Style(width=16))
          me.button(
            "Prefer right", type="raised", color="primary", on_click=reveal
          )

        if me.state(State).reveal:
          me.text(f"Left = {outputs[0].version} | Right = {outputs[1].version}")


def output_ui(output: Output):
  with me.box(
    style=me.Style(
      background="#f0f4f8",
      padding=me.Padding(top=16, bottom=16, left=24, right=24),
    )
  ):
    content_style = me.Style(
      width="min(100%, 70ch)",
      margin=me.Margin(left="auto", right="auto", bottom=16),
      background="#fff",
      padding=me.Padding(top=16, bottom=16, left=16, right=16),
      border_radius=12,
      line_height="1.5",
      letter_spacing="0.07px",
    )
    with me.box(style=content_style):
      me.markdown(output.content)
