from dataclasses import field

import mesop as me


def compute():
  return "abc"


@me.stateclass
class State:
  count: int = 0
  string: str = compute()
  keys: list[str] = field(default_factory=list)


def checkbox_update(action: me.CheckboxChangeEvent) -> None:
  state = me.state(State)
  if action.checked:
    state.keys.append(action.key)
    state.string = "checked"
  else:
    state.keys.remove(action.key)
    state.string = "unchecked"


def button_click(action: me.ClickEvent):
  state = me.state(State)
  state.count += 1


@me.page(path="/many_checkboxes")
def main():
  state = me.state(State)
  me.button("click me", on_click=button_click)
  me.text(text=f"{state.count} clicks")
  me.text(text=f"Selected keys: {state.keys}")
  for i in range(100):
    me.checkbox(
      "check",
      on_change=checkbox_update,
      key=f"check={i}",
    )
  me.text(text=state.string)


@me.page(path="/other")
def other():
  me.text(text="other page")
