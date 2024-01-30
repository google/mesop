from matplotlib.figure import Figure

import mesop as me


@me.page(path="/integrations/matplotlib_grid")
def app():
  with me.box(
    style=me.Style(
      display="grid",
      grid_template_columns="1fr 1fr",
      gap="16px",
      padding=me.Padding(
        top=16,
        left=16,
        right=16,
        bottom=16,
      ),
      overflow_y="auto",
    )
  ):
    graph()
    graph()
    graph()
    graph()


def graph():
  border_side = me.BorderSide(width=1, color="#ddd", style="solid")
  with me.box(
    style=me.Style(
      background="#fff",
      border=me.Border(
        top=border_side,
        right=border_side,
        bottom=border_side,
        left=border_side,
      ),
      border_radius=16,
      padding=me.Padding(
        top=16,
        left=16,
        right=16,
        bottom=16,
      ),
    )
  ):
    # Create matplotlib figure without using pyplot:
    fig = Figure()
    ax = fig.subplots()  # type: ignore
    ax.plot([1, 2])  # type: ignore

    me.text("Example using matplotlib:")
    me.plot(fig, style=me.Style(width="100%"))
