import mesop.labs as mel


@mel.web_component(path="./web_component.js")
def web_component(array: list[str], object: dict[str, str]):
  return mel.insert_web_component(
    name="complex-prop-component",
    properties={
      "array": array,
      "object": object,
    },
  )
