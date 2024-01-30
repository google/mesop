from matplotlib.figure import Figure

import mesop as me


@me.page(path="/integrations/matplotlib")
def app():
  # Create matplotlib figure without using pyplot:
  fig = Figure()
  ax = fig.subplots()  # type: ignore
  ax.plot([1, 2])  # type: ignore

  me.text("Example using matplotlib:")
  me.plot(fig)

  me.text("Resize plot:")
  me.plot(fig, style=me.Style(width=200, height=200))
