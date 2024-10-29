import base64

import mesop as me


@me.stateclass
class State:
  file: me.UploadedFile
  upload_count: int = 0


@me.page(path="/components/uploader/e2e/content_uploader_app")
def app():
  state = me.state(State)
  with me.box(style=me.Style(padding=me.Padding.all(15))):
    with me.content_uploader(
      accepted_file_types=["image/jpeg", "image/png"],
      on_upload=handle_upload,
      type="flat",
      color="primary",
      style=me.Style(font_weight="bold"),
    ):
      with me.box(style=me.Style(display="flex", gap=5)):
        me.icon("upload")
        me.text("Upload Image", style=me.Style(line_height="25px"))

    if state.file.size:
      with me.box(style=me.Style(margin=me.Margin.all(10))):
        me.text(f"File name: {state.file.name}")
        me.text(f"File size: {state.file.size}")
        me.text(f"File type: {state.file.mime_type}")
        me.text(f"Upload count: {state.upload_count}")

      with me.box(style=me.Style(margin=me.Margin.all(10))):
        me.image(src=_convert_contents_data_url(state.file))


def handle_upload(event: me.UploadEvent):
  state = me.state(State)
  state.file = event.file
  state.upload_count += 1


def _convert_contents_data_url(file: me.UploadedFile) -> str:
  return (
    f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
  )
