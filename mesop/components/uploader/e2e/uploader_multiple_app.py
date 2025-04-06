import base64

import mesop as me


@me.stateclass
class State:
  files: list[me.UploadedFile]


@me.page(path="/components/uploader/e2e/uploader_multiple_app")
def app():
  state = me.state(State)
  with me.box(style=me.Style(padding=me.Padding.all(15))):
    me.uploader(
      label="Upload Image",
      accepted_file_types=["image/jpeg", "image/png"],
      on_upload=handle_upload,
      type="flat",
      color="primary",
      multiple=True,
      style=me.Style(font_weight="bold"),
    )

    if state.files:
      for file in state.files:
        with me.box(style=me.Style(margin=me.Margin.all(10))):
          me.text(f"File name: {file.name}")
          me.text(f"File size: {file.size}")
          me.text(f"File type: {file.mime_type}")

          with me.box(style=me.Style(margin=me.Margin.all(10))):
            me.image(src=_convert_contents_data_url(file))


def handle_upload(event: me.UploadEvent):
  state = me.state(State)
  state.files = event.files


def _convert_contents_data_url(file: me.UploadedFile) -> str:
  return (
    f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
  )
