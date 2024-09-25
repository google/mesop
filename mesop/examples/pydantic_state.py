from pydantic import BaseModel

import mesop as me


class PydanticModel(BaseModel):
  name: str = "World"
  counter: int = 0


@me.stateclass
class State:
  model: PydanticModel


@me.page(path="/pydantic_state")
def main():
  state = me.state(State)
  me.text(f"Name: {state.model.name}")
  me.text(f"Counter: {state.model.counter}")

  me.button("Increment Counter", on_click=on_click)


def on_click(e: me.ClickEvent):
  state = me.state(State)
  state.model.counter += 1
