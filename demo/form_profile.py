from dataclasses import asdict
from typing import Literal

import mesop as me

ROW_GAP = 15
BOX_PADDING = 20


def load(e: me.LoadEvent):
  me.set_theme_density(-3)
  me.set_theme_mode("system")


@me.stateclass
class State:
  first_name: str
  last_name: str
  username: str
  email: str
  facebook: str
  google: str
  instagram: str
  tiktok: str
  errors: dict[str, str]


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/form_profile",
  on_load=load,
)
def page():
  with me.box(
    style=me.Style(
      padding=me.Padding.all(BOX_PADDING),
      max_width=1000,
      margin=me.Margin.symmetric(horizontal="auto"),
    )
  ):
    me.text(
      "Profile",
      type="headline-4",
      style=me.Style(margin=me.Margin(bottom=15)),
    )

    divider()

    with form_group(
      label="Full name",
      description="This will be displayed on your profile.",
    ):
      input_field(label="First name")
      input_field(label="Last name")

    divider()

    with form_group(label="Account", description="This info must be unique."):
      input_field(label="Username")
      input_field(label="Email", input_type="email")

    divider()

    with form_group(
      label="Social media", description="Links to your social media profiles"
    ):
      input_field(label="Facebook", input_type="url")
      input_field(key="google", label="Google+", input_type="url")
      input_field(label="Instagram", input_type="url")
      input_field(label="TikTok", input_type="url")

    divider()

    me.button(
      "Save Profile",
      type="flat",
      on_click=on_click,
      style=me.Style(padding=me.Padding.all(25), font_size=20),
    )


def divider():
  with me.box(style=me.Style(margin=me.Margin.symmetric(vertical=20))):
    me.divider()


@me.content_component
def form_group(
  label: str = "",
  description: str = "",
):
  with me.box(
    style=me.Style(display="flex", gap=25, margin=me.Margin(bottom=20))
  ):
    with me.box(style=me.Style(flex_basis="200px")):
      me.text(label, type="headline-6", style=me.Style(font_weight="bold"))
      me.text(description, style=me.Style(font_style="italic", font_size=13))
    with me.box(
      style=me.Style(
        display="flex", flex_grow=1, flex_direction="column", width="100%"
      )
    ):
      me.slot()


def input_field(
  *,
  key: str = "",
  label: str,
  value: str = "",
  width: str | int = "100%",
  input_type: Literal[
    "color",
    "date",
    "datetime-local",
    "email",
    "month",
    "number",
    "password",
    "search",
    "tel",
    "text",
    "time",
    "url",
    "week",
  ] = "text",
):
  state = me.state(State)
  key = key if key else label.lower().replace(" ", "_")
  with me.box(style=me.Style(flex_grow=1, width=width)):
    me.input(
      key=key,
      label=label,
      value=value,
      appearance="outline",
      style=me.Style(width=width),
      type=input_type,
      on_blur=on_blur,
    )
    if key in state.errors:
      me.text(
        state.errors[key],
        style=me.Style(
          margin=me.Margin(top=-13, left=15, bottom=15),
          color=me.theme_var("error"),
          font_size=13,
        ),
      )


def on_change(e: me.RadioChangeEvent):
  state = me.state(State)
  setattr(state, e.key, e.value)


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  setattr(state, e.key, e.value)


def on_click(e: me.ClickEvent):
  state = me.state(State)

  # Replace with real validation logic.
  errors = {}
  for key, value in asdict(state).items():  # type: ignore
    if key == "error":
      continue
    if not value:
      errors[key] = f"{key.replace('_', ' ').capitalize()} is required"
  state.errors = errors

  # Replace with form processing logic.
  if not state.errors:
    pass
