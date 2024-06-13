from io import BytesIO
from typing import Protocol
from mesop.component_helpers import Style, component
from mesop.components.html.html import html


class figure(Protocol):
  """
  Provides a minimal interface based on bokeh's Figure class.
  """

  def savefig(self, fname: BytesIO, *, format: str):
    pass


# Skip pydantic validation because Figure is a Protocol which can't type-check properly
@component(skip_validation=True)
def bokeh_plot(figure: figure, *, style: Style | None = None):
  """
  Creates a plot component from a Bokeh figure.

  Args:
    figure: A [Bokeh figure](https://docs.bokeh.org/en/latest/docs/reference/plotting/figure.html) which will be rendered.
    style: An optional Style object that defines the visual styling for the
      plot component. If None, default styling (e.g. height, width) is used.
  """
  from bokeh.embed import file_html
  html(file_html(figure, "inline"), style=style)
