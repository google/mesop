from dataclasses import dataclass
from typing import Any, Callable, Literal, Sequence

import mesop.components.uploader.uploader_pb2 as uploader_pb
from mesop.component_helpers import (
  Style,
  component,
  insert_composite_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.components.text.text import text
from mesop.components.uploader.uploaded_file import UploadedFile
from mesop.events import MesopEvent
from mesop.exceptions import MesopDeveloperException


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


@component
def uploader(
  *,
  label: str,
  accepted_file_types: Sequence[str] | None = None,
  key: str | None = None,
  on_upload: Callable[[UploadEvent], Any] | None = None,
  type: Literal["raised", "flat", "stroked"] | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  disable_ripple: bool = False,
  disabled: bool = False,
  style: Style | None = None,
):
  """Creates an uploader with a simple text Button component.

  Args:
      label: Uploader button text.
      accepted_file_types: List of accepted file types. See the [accept parameter](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#accept).
      key: The component [key](../components/index.md#component-key).
      on_upload: File upload event handler.
      type: Type of button style to use.
      color: Theme color palette of the button.
      disable_ripple: Whether the ripple effect is disabled or not.
      disabled: Whether the button is disabled.
      style: Style for the component.
  """
  with content_uploader(
    on_upload=on_upload,
    accepted_file_types=accepted_file_types,
    type=type,
    color=color,
    disable_ripple=disable_ripple,
    disabled=disabled,
    style=style,
    key=key,
  ):
    text(label)


@register_native_component
def content_uploader(
  *,
  accepted_file_types: Sequence[str] | None = None,
  key: str | None = None,
  on_upload: Callable[[UploadEvent], Any] | None = None,
  type: Literal["raised", "flat", "stroked", "icon"] | None = None,
  color: Literal["primary", "accent", "warn"] | None = None,
  disable_ripple: bool = False,
  disabled: bool = False,
  style: Style | None = None,
):
  """
  Creates an uploader component, which is a composite component. Typically, you would
  use a text or icon component as a child.

  Intended for advanced use cases.

  Args:
      accepted_file_types: List of accepted file types. See the [accept parameter](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#accept).
      key: The component [key](../components/index.md#component-key).
      on_upload: File upload event handler.
      type: Type of button style to use
      color: Theme color palette of the button
      disable_ripple: Whether the ripple effect is disabled or not.
      disabled: Whether the button is disabled.
      style: Style for the component.
  """
  return insert_composite_component(
    key=key,
    type_name="content_uploader",
    proto=uploader_pb.UploaderType(
      accepted_file_type=accepted_file_types or [],
      on_upload_event_handler_id=register_event_handler(
        on_upload, event=UploadEvent
      )
      if on_upload
      else "",
      type_index=_get_type_index(type),
      type=type,
      color=color,
      disable_ripple=disable_ripple,
      disabled=disabled,
    ),
    style=style,
  )


def _get_type_index(
  type: Literal["raised", "flat", "stroked", "icon"] | None,
) -> int:
  if type is None:
    return 0
  if type == "raised":
    return 1
  if type == "flat":
    return 2
  if type == "stroked":
    return 3
  if type == "icon":
    return 4
  raise Exception("Unexpected type: " + type)
