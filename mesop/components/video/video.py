import mesop.components.video.video_pb2 as video_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def video(
  *,
  src: str,
  style: Style | None = None,
  key: str | None = None,
):
  """
  Creates a video.

  Args:
      src: URL of the video source
      style: The style to apply to the image, such as width and height.
  """
  insert_component(
    key=key,
    type_name="video",
    proto=video_pb.VideoType(
      src=src,
    ),
    style=style,
  )
