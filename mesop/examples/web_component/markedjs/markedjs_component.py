import mesop as me


@me.web_component(path="./markedjs_component.js")
def markedjs_component(markdown: str):
  return me.insert_web_component(
    name="markedjs-component",
    properties={
      "markdown": markdown,
    },
  )
