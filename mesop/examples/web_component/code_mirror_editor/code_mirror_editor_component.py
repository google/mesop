from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./code_mirror_editor_component.js")
def code_mirror_editor_component(
  *,
  code: str = "",
  on_editor_blur: Callable[[mel.WebEvent], Any] | None = None,
  height: str = "100%",
  width: str = "100%",
  key: str | None = None,
):
  events = {}
  if on_editor_blur:
    events["editorBlurEvent"] = on_editor_blur

  return mel.insert_web_component(
    name="code-mirror-editor-component",
    key=key,
    events=events,
    properties={
      "code": code,
      "height": height,
      "width": width,
    },
  )
