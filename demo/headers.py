from dataclasses import fields

import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/headers",
)
def app():
  is_mobile = me.viewport_size().width < 640

  with me.box(style=me.Style(margin=me.Margin(bottom=15))):
    # Two section basic header with fluid width.
    # As an example, we don't use mobile view here since the header is short enough.
    with header(max_width=None):
      with header_section():
        me.text(
          "Mesop", type="headline-6", style=me.Style(margin=me.Margin(bottom=0))
        )

      with header_section():
        me.button("Home")
        me.button("About")
        me.button("FAQ")

  with me.box(style=me.Style(margin=me.Margin(bottom=15))):
    # Two section basic header.
    with header(is_mobile=is_mobile):
      with header_section():
        me.text(
          "Mesop", type="headline-6", style=me.Style(margin=me.Margin(bottom=0))
        )

      with header_section():
        me.button("Home")
        me.button("About")
        me.button("FAQ")

  with me.box(style=me.Style(margin=me.Margin(bottom=15))):
    # Three section basic header.
    with header(is_mobile=is_mobile):
      with header_section():
        me.text(
          "Mesop", type="headline-6", style=me.Style(margin=me.Margin(bottom=0))
        )

      with header_section():
        me.button("Home")
        me.button("About")
        me.button("FAQ")

      with header_section():
        me.button("Login", type="flat")

  with me.box(style=me.Style(margin=me.Margin(bottom=15))):
    # Centered header with overrides and icons
    with header(is_mobile=is_mobile, style=me.Style(justify_content="center")):
      with header_section():
        with me.content_button(
          style=me.Style(
            padding=me.Padding.symmetric(vertical=30, horizontal=25)
          )
        ):
          me.icon("home")
          me.text("Home")
        with me.content_button(
          style=me.Style(
            padding=me.Padding.symmetric(vertical=30, horizontal=25)
          )
        ):
          me.icon("info")
          me.text("About")
        with me.content_button(
          style=me.Style(
            padding=me.Padding.symmetric(vertical=30, horizontal=25)
          )
        ):
          me.icon("contact_support")
          me.text("FAQ")
        with me.content_button(
          style=me.Style(
            padding=me.Padding.symmetric(vertical=30, horizontal=25)
          )
        ):
          me.icon("login")
          me.text("Login")

  with me.box(style=me.Style(margin=me.Margin(bottom=15))):
    # Header with overridden background
    with header(
      is_mobile=is_mobile, style=me.Style(background="#0F0F11", color="#E3E3E3")
    ):
      with header_section():
        me.text(
          "Mesop", type="headline-6", style=me.Style(margin=me.Margin(bottom=0))
        )

      with header_section():
        me.button("Home", type="stroked", style=me.Style(color="#E3E3E3"))
        me.button("About", type="stroked", style=me.Style(color="#E3E3E3"))
        me.button("FAQ", type="stroked", style=me.Style(color="#E3E3E3"))

      with header_section():
        me.button("Login", type="flat")


@me.content_component
def header(
  *,
  style: me.Style | None = None,
  is_mobile: bool = False,
  max_width: int | None = 1000,
):
  """Creates a simple header component.

  Args:
    style: Override the default styles, such as background color, etc.
    is_mobile: Use mobile layout. Arranges each section vertically.
    max_width: Sets the maximum width of the header. Use None for fluid header.
  """
  default_flex_style = (
    _DEFAULT_MOBILE_FLEX_STYLE if is_mobile else _DEFAULT_FLEX_STYLE
  )
  if max_width and me.viewport_size().width >= max_width:
    default_flex_style = merge_styles(
      default_flex_style,
      me.Style(width=max_width, margin=me.Margin.symmetric(horizontal="auto")),
    )

  # The style override is a bit hacky here since we apply the override styles to both
  # boxes here which could cause problems depending on what styles are added.
  with me.box(style=merge_styles(_DEFAULT_STYLE, style)):
    with me.box(style=merge_styles(default_flex_style, style)):
      me.slot()


@me.content_component
def header_section():
  """Adds a section to the header."""
  with me.box(style=me.Style(display="flex", gap=5)):
    me.slot()


def merge_styles(
  default: me.Style, overrides: me.Style | None = None
) -> me.Style:
  """Merges two styles together.

  Args:
    default: The starting style
    overrides: Any set styles will override styles in default
  """
  if not overrides:
    overrides = me.Style()

  default_fields = {
    field.name: getattr(default, field.name) for field in fields(me.Style)
  }
  override_fields = {
    field.name: getattr(overrides, field.name)
    for field in fields(me.Style)
    if getattr(overrides, field.name) is not None
  }

  return me.Style(**default_fields | override_fields)


_DEFAULT_STYLE = me.Style(
  background=me.theme_var("surface-container"),
  border=me.Border.symmetric(
    vertical=me.BorderSide(
      width=1,
      style="solid",
      color=me.theme_var("outline-variant"),
    )
  ),
  padding=me.Padding.all(10),
)

_DEFAULT_FLEX_STYLE = me.Style(
  align_items="center",
  display="flex",
  gap=5,
  justify_content="space-between",
)

_DEFAULT_MOBILE_FLEX_STYLE = me.Style(
  align_items="center",
  display="flex",
  flex_direction="column",
  gap=12,
  justify_content="center",
)
