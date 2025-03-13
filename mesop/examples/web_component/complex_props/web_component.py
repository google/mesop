import mesop as me


@me.web_component(path="./web_component.js")
def web_component(array: list[str], object: dict[str, str]):
  return me.insert_web_component(
    name="complex-prop-component",
    properties={
      "array": array,
      "object": object,
    },
  )
