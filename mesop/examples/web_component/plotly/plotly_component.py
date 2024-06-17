import mesop.labs as mel


@mel.web_component(path="./plotly_component.js")
def plotly_component():
  return mel.insert_web_component(name="plotly-component")
