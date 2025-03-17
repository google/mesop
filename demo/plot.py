from matplotlib.figure import Figure

import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/plot",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    # Create matplotlib figure without using pyplot:
    fig = Figure()
    ax = fig.subplots()  # type: ignore
    ax.plot([1, 2])  # type: ignore

    me.text("Example using matplotlib:", type="headline-5")
    me.plot(fig, style=me.Style(width="100%"))
