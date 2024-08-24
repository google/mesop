from functools import partial

import mesop as me


@me.stateclass
class State:
  count: int = 0


@me.page(path="/functools_partial")
def main():
  state = me.state(State)
  me.text(text=f"value={state.count}")
  me.button("increment 2*4", on_click=partial(increment_click, 2, amount=4))
  me.button("increment 2*10", on_click=partial(increment_click, 2, amount=10))
  for i in range(10):
    me.button(f"decrement {i}", on_click=partial(decrement_click, i))


def increment_click(multiplier: int, action: me.ClickEvent, amount: int):
  state = me.state(State)
  state.count += multiplier * amount


def decrement_click(amount: int, action: me.ClickEvent):
  state = me.state(State)
  state.count -= amount
