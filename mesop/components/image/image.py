import mesop.components.image.image_pb2 as image_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_native_component,
)


@register_native_component
def image(
  *,
  src: str | None = None,
  alt: str | None = None,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates an image component.

  Args:
      src: The source URL of the image.
      alt: The alternative text for the image if it cannot be displayed.
      style: The style to apply to the image, such as width and height.
      key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="image",
    proto=image_pb.ImageType(
      src=src,
      alt=alt,
    ),
    style=style,
  )
