import mesop as me


@me.web_component(path="./outer_component.js")
def outer_component(
  *,
  key: str | None = None,
):
  return me.insert_web_component(
    name="dynamic-slot-outer-component",
    key=key,
  )


@me.web_component(path="./outer_component2.js")
def outer_component2(
  *,
  key: str | None = None,
):
  return me.insert_web_component(
    name="dynamic-slot-outer-component2",
    key=key,
  )
