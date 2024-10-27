import mesop.labs as mel


@mel.web_component(path="./outer_component.js")
def outer_component(
  *,
  key: str | None = None,
):
  return mel.insert_web_component(
    name="dynamic-slot-outer-component",
    key=key,
  )


@mel.web_component(path="./outer_component2.js")
def outer_component2(
  *,
  key: str | None = None,
):
  return mel.insert_web_component(
    name="dynamic-slot-outer-component2",
    key=key,
  )
