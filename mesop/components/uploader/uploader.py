import io
from dataclasses import dataclass
from typing import Any, Callable, Sequence

import mesop.components.uploader.uploader_pb2 as uploader_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent
from mesop.exceptions import MesopDeveloperException


class UploadedFile(io.BytesIO):
  """Uploaded file contents and metadata."""

  def __init__(self, contents: bytes, *, name: str, size: int, mime_type: str):
    super().__init__(contents)
    self._name = name
    self._size = size
    self._mime_type = mime_type

  @property
  def name(self):
    return self._name

  @property
  def size(self):
    return self._size

  @property
  def mime_type(self):
    return self._mime_type


@dataclass(kw_only=True)
class UploadEvent(MesopEvent):
  """Event for file uploads.

  Attributes:
      file: Uploaded file.
  """

  file: UploadedFile


def map_upload_event(event, key):
  upload_event = uploader_pb.UploadEvent()
  upload_event.ParseFromString(event.bytes_value)
  if upload_event.file:
    return UploadEvent(
      key=key.key,
      file=UploadedFile(
        upload_event.file[0].contents,
        name=upload_event.file[0].name,
        size=upload_event.file[0].size,
        mime_type=upload_event.file[0].mime_type,
      ),
    )
  raise MesopDeveloperException("No file was sent to the server.")


register_event_mapper(UploadEvent, map_upload_event)


@register_native_component
def uploader(
  *,
  label: str,
  accepted_file_types: Sequence[str] | None = None,
  key: str | None = None,
  on_upload: Callable[[UploadEvent], Any] | None = None,
):
  """
  This function creates an uploader.

  Args:
      label: Upload button label.
      accepted_file_types: List of accepted file types. See the [accept parameter](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#accept).
      on_upload: File upload event handler.
  """
  insert_component(
    key=key,
    type_name="uploader",
    proto=uploader_pb.UploaderType(
      label=label,
      accepted_file_type=accepted_file_types or [],
      on_upload_event_handler_id=register_event_handler(
        on_upload, event=UploadEvent
      )
      if on_upload
      else "",
    ),
  )
