import mesop.labs as mel


@mel.web_component(path="./markedjs_component.js")
def markedjs_component(markdown: str):
  return mel.insert_web_component(
    name="markedjs-component",
    properties={
      "markdown": markdown,
    },
  )
