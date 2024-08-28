import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  with me.box(
    style=me.Style(display="grid", gap=16, padding=me.Padding.all(16))
  ):
    with me.box(
      style=me.Style(
        padding=me.Padding.all(16),
        border_radius=8,
        background=me.theme_var("surface"),
      )
    ):
      me.button("Learn More", type="flat", on_click=learn_more)

    with me.box(
      style=me.Style(
        padding=me.Padding.all(16),
        border_radius=8,
        background=me.theme_var("surface"),
      )
    ):
      me.text("Grid Item 1", type="headline-5")

    with me.box(
      style=me.Style(
        padding=me.Padding.all(16),
        border_radius=8,
        background=me.theme_var("surface"),
      )
    ):
      me.text("Grid Item 2", type="headline-5")

    with me.box(
      style=me.Style(
        padding=me.Padding.all(16),
        border_radius=8,
        background=me.theme_var("surface"),
      )
    ):
      me.text("Grid Item 3", type="headline-5")


def learn_more(event: me.ClickEvent):
  print("Learn more button clicked!")


def update_text(event: me.InputEvent):
  print("Text updated:", event.value)
