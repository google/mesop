import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/chat_inputs",
)
def app():
  with me.box(style=CONTENT_STYLE):
    subtle_chat_input()
    elevated_chat_input()

    me.textarea(
      placeholder="Default chat input",
      style=me.Style(width="100%"),
      rows=2,
    )


@me.component
def subtle_chat_input():
  with me.box(
    style=me.Style(
      border_radius=16,
      padding=me.Padding.all(8),
      background=BACKGROUND_COLOR,
      display="flex",
      width="100%",
    )
  ):
    with me.box(
      style=me.Style(
        flex_grow=1,
      )
    ):
      me.native_textarea(
        autosize=True,
        min_rows=4,
        placeholder="Subtle chat input",
        style=me.Style(
          padding=me.Padding(top=16, left=16),
          background=BACKGROUND_COLOR,
          outline="none",
          width="100%",
          overflow_y="auto",
          border=me.Border.all(
            me.BorderSide(style="none"),
          ),
        ),
      )
    with me.content_button(type="icon"):
      me.icon("upload")
    with me.content_button(type="icon"):
      me.icon("photo")
    with me.content_button(type="icon"):
      me.icon("send")


@me.component
def elevated_chat_input():
  with me.box(
    style=me.Style(
      padding=me.Padding.all(8),
      background="white",
      display="flex",
      width="100%",
      border=me.Border.all(
        me.BorderSide(width=0, style="solid", color="black")
      ),
      box_shadow="0 10px 20px #0000000a, 0 2px 6px #0000000a, 0 0 1px #0000000a",
    )
  ):
    with me.box(
      style=me.Style(
        flex_grow=1,
      )
    ):
      me.native_textarea(
        autosize=True,
        min_rows=4,
        placeholder="Elevated chat input",
        style=me.Style(
          font_family="monospace",
          padding=me.Padding(top=16, left=16),
          background="white",
          outline="none",
          width="100%",
          overflow_y="auto",
          border=me.Border.all(
            me.BorderSide(style="none"),
          ),
        ),
      )
    with me.content_button(type="icon"):
      me.icon("upload")
    with me.content_button(type="icon"):
      me.icon("photo")
    with me.content_button(type="icon"):
      me.icon("send")


BACKGROUND_COLOR = "#e2e8f0"

CONTENT_STYLE = me.Style(padding=me.Padding.all(16), gap=16, display="grid")
