from dataclasses import field

import optic as op


def compute():
  return "abc"


@op.stateclass
class State:
  count: int = 0
  string: str = compute()
  keys: list[str] = field(default_factory=list)


@op.on(op.CheckboxEvent)
def checkbox_update(action: op.CheckboxEvent) -> None:
  state = op.state(State)
  if action.checked:
    state.keys.append(action.key.key)
    state.string = "checked"
  else:
    state.keys.remove(action.key.key)
    state.string = "unchecked"


@op.on(op.ClickEvent)
def button_click(action: op.ClickEvent):
  state = op.state(State)
  state.count += 1


@op.page()
def main():
  state = op.state(State)
  op.button(label="click me", on_click=button_click)
  op.text(text=f"{state.count} clicks")
  state.keys
  op.text(text=f"Selected keys: {state.keys}")
  for i in range(1000):
    op.checkbox(
      label=f"check {i}?", on_update=checkbox_update, key=f"check={i}"
    )
  op.text(text=state.string)


@op.page(path="/other")
def other():
  op.text(text="other page")
