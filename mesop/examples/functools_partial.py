from functools import partial

import mesop as me


@me.stateclass
class State:
  count: int = 0


@me.page(path="/functools_partial")
def main():
  state = me.state(State)
  me.text(text=f"{state.count}")
  me.button("increment 2*4", on_click=partial(increment_click, 2, amount=4))
  me.button("increment 2*10", on_click=partial(increment_click, 2, amount=10))


def increment_click(multiplier: int, action: me.ClickEvent, amount: int):
  state = me.state(State)
  state.count += multiplier * amount
