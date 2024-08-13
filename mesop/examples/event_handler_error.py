import asyncio
import time
from typing import Generator

import mesop as me


@me.page(path="/event_handler_error")
def page():
  me.text("Hello, world!")
  me.button(label="Regular event handler", on_click=on_click)
  me.button(label="Generator event handler", on_click=on_click_generator)
  me.button(label="Yield from event handler", on_click=on_click_yield_from)
  me.button(
    label="Async generator event handler", on_click=on_click_async_generator
  )


def on_click(e: me.ClickEvent):
  raise Exception("Error in on_click.")


def on_click_generator(e: me.ClickEvent):
  yield
  raise Exception("Error in on_click_generator.")


def on_click_yield_from(e: me.ClickEvent) -> Generator[None, None, None]:
  yield from a_generator()


def a_generator():
  yield
  time.sleep(0.2)
  raise Exception("Error in a_generator.")


async def on_click_async_generator(e: me.ClickEvent):
  await asyncio.sleep(0.2)
  yield
  raise Exception("Error in on_click_async_generator.")
