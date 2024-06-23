import mesop as me  # noqa: I001
import simple_slot_app  # type: ignore  # noqa: F401


@me.stateclass
class State:
  count_clicks: int = 0


def button_click(event: me.ClickEvent):
  state = me.state(State)
  state.count_clicks += 1


@me.page(path="/buttons")
def main():
  me.text("Running mesop version: " + me.__version__)
  state = me.state(State)

  me.button(
    "Button",
    on_click=button_click,
    type="flat",
    color="primary",
  )

  me.text(text=f"{state.count_clicks} clicks")
