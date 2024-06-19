from bokeh.plotting import figure
from bokeh.sampledata.penguins import data
from bokeh.transform import factor_cmap, factor_mark

import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/bokeh_plot",
)
def app():
  # Create bokeh figure
  SPECIES = sorted(data.species.unique())
  MARKERS = ["hex", "circle_x", "triangle"]

  p = figure(title="Penguin size", background_fill_color="#fafafa")
  p.xaxis.axis_label = "Flipper Length (mm)"
  p.yaxis.axis_label = "Body Mass (g)"

  p.scatter(
    "flipper_length_mm",
    "body_mass_g",
    source=data,
    legend_group="species",
    fill_alpha=0.4,
    size=12,
    marker=factor_mark("species", MARKERS, SPECIES),
    color=factor_cmap("species", "Category10_3", SPECIES),
  )

  p.legend.location = "top_left"
  p.legend.title = "Species"

  me.text("Example using bokeh:")
  me.bokeh_plot(p, style=me.Style(width="100%"))
