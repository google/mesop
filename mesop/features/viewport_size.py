from dataclasses import dataclass

from mesop.runtime import runtime


@dataclass(kw_only=True)
class Size:
  """
  Attributes:
      width: The width of the viewport in pixels.
      height: The height of the viewport in pixels.
  """

  width: int
  height: int


def viewport_size() -> Size:
  """
  Returns the current viewport size.

  Returns:
      Size: The current viewport size.
  """
  pb_size = runtime().context().viewport_size()
  return Size(
    width=pb_size.width,
    height=pb_size.height,
  )
