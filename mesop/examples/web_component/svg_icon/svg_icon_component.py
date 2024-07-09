import mesop.labs as mel


@mel.web_component(path="./svg_icon_component.js")
def svg_icon(
  *,
  svg: str | None = None,
  key: str | None = None,
):
  return mel.insert_web_component(
    name="svg-icon",
    key=key,
    properties={"svg": svg},
  )
