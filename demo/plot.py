from matplotlib.figure import Figure

import mesop as me


@me.page(path="/plot")
def app():
  # Create matplotlib figure without using pyplot:
  fig = Figure()
  ax = fig.subplots()  # type: ignore
  ax.plot([1, 2])  # type: ignore

  me.text("Example using matplotlib:")
  me.plot(fig, style=me.Style(width="100%"))
