import base64
from io import BytesIO
from typing import Protocol

from mesop.component_helpers import Style, component
from mesop.components.image.image import image


class Figure(Protocol):
  """
  Provides a minimal interface based on matplotlib's Figure class.
  """

  def savefig(self, fname: BytesIO, *, format: str):
    pass


# Skip pydantic validation because Figure is a Protocol which can't type-check properly
@component(skip_validation=True)
def plot(figure: Figure, *, style: Style | None = None):
  """
  Creates a plot component from a Matplotlib figure.

  Args:
    figure: A [Matplotlib figure](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure) which will be rendered.
    style: An optional Style object that defines the visual styling for the
      plot component. If None, default styling (e.g. height, width) is used.
  """
  buf = BytesIO()
  figure.savefig(buf, format="svg")
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  image(src=f"data:image/svg+xml;base64,{data}", style=style)
