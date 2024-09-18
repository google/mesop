from dataclasses import field
from datetime import date

import mesop as me


@me.stateclass
class State:
  picked_date: date | None = field(default_factory=lambda: date(2024, 10, 1))
  picked_start_date: date | None = field(
    default_factory=lambda: date(2024, 10, 1)
  )
  picked_end_date: date | None = field(
    default_factory=lambda: date(2024, 11, 1)
  )


@me.page(path="/components/datepicker/e2e/datepicker_app")
def app():
  state = me.state(State)
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=15,
      padding=me.Padding.all(15),
    )
  ):
    me.date_picker(
      label="Date",
      disabled=False,
      placeholder="9/12/2024",
      required=True,
      value=state.picked_date,
      readonly=False,
      hide_required_marker=False,
      color="accent",
      float_label="always",
      appearance="outline",
      on_change=on_date_change,
    )

    me.text("Selected date: " + _render_date(state.picked_date))

    me.divider()

    me.date_range_picker(
      label="Date Range",
      disabled=False,
      placeholder_start_date="9/12/2024",
      placeholder_end_date="10/12/2024",
      required=True,
      value_start_date=state.picked_start_date,
      value_end_date=state.picked_end_date,
      readonly=False,
      hide_required_marker=False,
      color="accent",
      float_label="always",
      appearance="outline",
      on_change=on_date_range_change,
    )

    me.text("Start date: " + _render_date(state.picked_start_date))
    me.text("End date: " + _render_date(state.picked_end_date))


def on_date_change(e: me.DatePickerChangeEvent):
  state = me.state(State)
  state.picked_date = e.date


def on_date_range_change(e: me.DateRangePickerChangeEvent):
  state = me.state(State)
  state.picked_start_date = e.start_date
  state.picked_end_date = e.end_date


def _render_date(maybe_date: date | None) -> str:
  if maybe_date:
    return maybe_date.strftime("%Y-%m-%d")
  return "None"
