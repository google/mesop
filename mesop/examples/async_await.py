import asyncio

import mesop as me


@me.page(path="/async_await")
def page():
  s = me.state(State)
  me.text("val1=" + s.val1)
  me.text("val2=" + s.val2)
  me.button("async with yield", on_click=click_async_with_yield)
  me.button("async without yield", on_click=click_async_no_yield)


@me.stateclass
class State:
  val1: str
  val2: str


async def fetch_dummy_values():
  # Simulate an asynchronous operation
  await asyncio.sleep(2)
  return "<async_value>"


async def click_async_with_yield(e: me.ClickEvent):
  val1_task = asyncio.create_task(fetch_dummy_values())
  val2_task = asyncio.create_task(fetch_dummy_values())

  me.state(State).val1, me.state(State).val2 = await asyncio.gather(
    val1_task, val2_task
  )
  yield


async def click_async_no_yield(e: me.ClickEvent):
  val1_task = asyncio.create_task(fetch_dummy_values())
  val2_task = asyncio.create_task(fetch_dummy_values())

  me.state(State).val1, me.state(State).val2 = await asyncio.gather(
    val1_task, val2_task
  )
