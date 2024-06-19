import mesop as me


@me.page(path="/components/bokeh_plot/e2e/bokeh_plot_app")
def app():
  from bokeh.plotting import figure

  f = figure()
  f.title.text = "BOKEH_E2E_FIGURE"
  # Added bokeh plot with title text BOKEH_E2E_FIGURE
  me.bokeh_plot(f)
