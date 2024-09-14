from dataclasses import asdict
from typing import Literal

import mesop as me

ROW_GAP = 15
BOX_PADDING = 20


@me.stateclass
class State:
  first_name: str
  last_name: str
  username: str
  email: str
  address: str
  address_2: str
  country: str
  state: str
  zip: str
  payment_type: str
  name_on_card: str
  credit_card: str
  expiration: str
  cvv: str
  errors: dict[str, str]


def is_mobile():
  return me.viewport_size().width < 620


def calc_input_size(items: int):
  return int(
    (me.viewport_size().width - (ROW_GAP * items) - (BOX_PADDING * 2)) / items
  )


def load(e: me.LoadEvent):
  me.set_theme_density(-3)
  me.set_theme_mode("system")


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/form_billing",
  on_load=load,
)
def page():
  state = me.state(State)

  with me.box(
    style=me.Style(
      padding=me.Padding.all(BOX_PADDING),
      max_width=800,
      margin=me.Margin.symmetric(horizontal="auto"),
    )
  ):
    me.text(
      "Billing form",
      type="headline-4",
      style=me.Style(margin=me.Margin(bottom=10)),
    )

    with form_group():
      name_width = calc_input_size(2) if is_mobile() else "100%"
      input_field(label="First name", width=name_width)
      input_field(label="Last name", width=name_width)

    with form_group():
      input_field(label="Username")

    with me.box(style=me.Style(display="flex", gap=ROW_GAP)):
      input_field(label="Email", input_type="email")

    with me.box(style=me.Style(display="flex", gap=ROW_GAP)):
      input_field(label="Address")

    with form_group():
      input_field(label="Address 2")

    with form_group():
      country_state_zip_width = calc_input_size(3) if is_mobile() else "100%"
      input_field(label="Country", width=country_state_zip_width)
      input_field(label="State", width=country_state_zip_width)
      input_field(label="Zip", width=country_state_zip_width)

    divider()

    me.text(
      "Payment",
      type="headline-4",
      style=me.Style(margin=me.Margin(bottom=10)),
    )

    with form_group(flex_direction="column"):
      me.radio(
        key="payment_type",
        on_change=on_change,
        options=[
          me.RadioOption(label="Credit card", value="credit_card"),
          me.RadioOption(label="Debit card", value="debit_card"),
          me.RadioOption(label="Paypal", value="paypal"),
        ],
        style=me.Style(
          display="flex", flex_direction="column", margin=me.Margin(bottom=20)
        ),
      )
      if "payment_type" in state.errors:
        me.text(
          state.errors["payment_type"],
          style=me.Style(
            margin=me.Margin(top=-30, left=5, bottom=15),
            color=me.theme_var("error"),
            font_size=13,
          ),
        )

    with form_group():
      payments_width = calc_input_size(2) if is_mobile() else "100%"
      input_field(label="Name on card", width=payments_width)
      input_field(label="Credit card", width=payments_width)

    with form_group():
      input_field(label="Expiration", width=payments_width)
      input_field(label="CVV", width=payments_width, input_type="number")

    divider()

    me.button(
      "Continue to checkout",
      type="flat",
      style=me.Style(width="100%", padding=me.Padding.all(25), font_size=20),
      on_click=on_click,
    )


def divider():
  with me.box(style=me.Style(margin=me.Margin.symmetric(vertical=20))):
    me.divider()


@me.content_component
def form_group(flex_direction: Literal["row", "column"] = "row"):
  with me.box(
    style=me.Style(
      display="flex", flex_direction=flex_direction, gap=ROW_GAP, width="100%"
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
