from dataclasses import dataclass, field
import optic as op


@dataclass
class State:
    string: str
    count: int
    keys: list[str] = field(default_factory=list)


store = op.store(
    State(string="init", count=0),
)


@op.on(op.CheckboxEvent)
def checkbox_update(state: State, action: op.CheckboxEvent) -> None:
    if action.checked:
        state.keys.append(action.key.key)
        state.string = "checked"
    else:
        state.keys.remove(action.key.key)
        state.string = "unchecked"


@op.on(op.ClickEvent)
def button_click(state: State, action: op.ClickEvent):
    state.count += 1


@op.page()
def main():
    state = store.get_state()
    op.button(label="click me", on_click=button_click)
    op.text(text=f"{state.count} clicks")
    state.keys
    op.text(text=f"Selected keys: {state.keys}")
    for i in range(1000):
        op.checkbox(label=f"check {i}?", on_update=checkbox_update, key=f"check={i}")
    op.text(text=state.string)


@op.page(path="/other")
def other():
    op.text(text="other page")
