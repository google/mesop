from typing import Literal

import mesop.components.html.html_pb2 as html_pb
from mesop.component_helpers import (
  Border,
  BorderSide,
  Style,
  insert_component,
  register_native_component,
)
from mesop.warn import warn


@register_native_component
def html(
  html: str = "",
  *,
  mode: Literal["sanitized", "sandboxed"] | None = None,
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function renders custom HTML in a secure way.

  Args:
      html: The HTML content to be rendered.
      mode: Determines how the HTML is rendered. Mode can be either "sanitized" or "sandboxed".
          If "sanitized" then potentially dangerous content like `<script>` and `<style>` are
          stripped out. If "sandboxed", then all content is allowed, but rendered in an iframe for isolation.
      style: The style to apply to the embed, such as width and height.
      key: The component [key](../components/index.md#component-key).
  """
  if mode != "sandboxed" and (
    any(
      activeContent in html
      for activeContent in ("<script>", "<style>", "style=")
    )
  ):
    warn(
      "Javascript or Stylesheets were sanitized from me.html. Use me.html(mode='sandboxed') instead."
    )
  if style is None:
    style = Style()
  if style.border is None:
    style.border = Border.all(
      BorderSide(
        width=0,
      )
    )
  insert_component(
    key=key,
    type_name="html",
    proto=html_pb.HtmlType(
      html=html,
      mode=mode,
    ),
    style=style,
  )
