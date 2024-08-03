import mesop as me
from mesop.examples.web_component.copy_to_clipboard.copy_to_clipboard_component import (
  copy_to_clipboard_component,
)

TEXT = """
Lorem ipsum odor amet, consectetuer adipiscing elit. Libero maecenas curae
porttitor laoreet quam proin phasellus. Efficitur hendrerit magnis volutpat sed
nascetur; turpis vitae dis. Phasellus suspendisse eleifend mus arcu scelerisque
quis. Eget venenatis diam dui mattis eleifend porttitor risus. Mollis eros
fermentum lectus magnis enim dapibus magna elit. Sapien gravida arcu fusce;
lacinia magnis donec. Nostra vulputate litora luctus id ut.
""".strip()


@me.page(
  path="/web_component/copy_to_clipboard/copy_to_clipboard_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
  ),
)
def page():
  with me.box(
    style=me.Style(
      width=300,
      margin=me.Margin.all(15),
      padding=me.Padding.all(10),
      border=me.Border.all(
        me.BorderSide(
          width=1, color=me.theme_var("outline-variant"), style="solid"
        )
      ),
    )
  ):
    with me.box(style=me.Style(display="flex", justify_content="end")):
      with copy_to_clipboard_component(text=TEXT):
        with me.content_button():
          me.icon("content_copy")
    me.text(TEXT)
