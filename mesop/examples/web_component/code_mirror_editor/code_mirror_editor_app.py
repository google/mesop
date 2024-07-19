import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.code_mirror_editor.code_mirror_editor_component import (
  code_mirror_editor_component,
)


@me.stateclass
class State:
  code: str = "# Add your Python code here."


@me.page(
  path="/web_component/code_mirror_editor/code_mirror_editor_app",
  stylesheets=[
    "https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.css"
  ],
  security_policy=me.SecurityPolicy(
    allowed_connect_srcs=[
      "https://cdnjs.cloudflare.com",
      "*.fonts.gstatic.com",
    ],
    allowed_script_srcs=["https://cdnjs.cloudflare.com", "*.fonts.gstatic.com"],
  ),
)
def page():
  state = me.state(State)
  with me.box(
    style=me.Style(
      display="grid",
      padding=me.Padding.all(20),
      gap=10,
      grid_template_rows="1fr 1fr",
      height="100vh",
    )
  ):
    code_mirror_editor_component(code=state.code, on_editor_blur=on_editor_blur)
    with me.box(style=me.Style(overflow_y="scroll", overflow_x="scroll")):
      me.text(
        "Type in some text in the editor. When the editor loses focus, the text below will be updated."
      )
      me.button(
        "Reset Code",
        type="flat",
        style=me.Style(margin=me.Margin.symmetric(vertical=30)),
        on_click=on_reset,
      )
      me.text("Code Output", type="headline-5")
      with me.box(
        style=me.Style(
          background="#fff",
          padding=me.Padding.all(20),
          border=me.Border.all(
            me.BorderSide(width=1, style="solid", color="#ececec")
          ),
        )
      ):
        me.code(state.code)


def on_reset(e: me.ClickEvent):
  state = me.state(State)
  state.code = "# Add your Python code here."


def on_editor_blur(e: mel.WebEvent):
  state = me.state(State)
  state.code = e.value["code"]
