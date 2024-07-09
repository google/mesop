import base64

import mesop as me


@me.stateclass
class State:
  name: str
  size: int
  mime_type: str
  contents: str


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/uploader",
)
def app():
  state = me.state(State)
  with me.box(style=me.Style(padding=me.Padding.all(15))):
    me.uploader(
      label="Upload Image",
      accepted_file_types=["image/jpeg", "image/png"],
      on_upload=handle_upload,
      type="flat",
      color="primary",
      style=me.Style(font_weight="bold"),
    )

    if state.contents:
      with me.box(style=me.Style(margin=me.Margin.all(10))):
        me.text(f"File name: {state.name}")
        me.text(f"File size: {state.size}")
        me.text(f"File type: {state.mime_type}")

      with me.box(style=me.Style(margin=me.Margin.all(10))):
        me.image(src=state.contents)


def handle_upload(event: me.UploadEvent):
  state = me.state(State)
  state.name = event.file.name
  state.size = event.file.size
  state.mime_type = event.file.mime_type
  state.contents = f"data:{event.file.mime_type};base64,{base64.b64encode(event.file.getvalue()).decode()}"
