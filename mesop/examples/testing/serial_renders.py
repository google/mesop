import mesop as me
import mesop.labs as mel


@me.stateclass
class State:
  count: int


@me.page(path="/testing/serial_renders")
def main():
  me.text(text=f"render={me.state(State).count}")
  me.button(label="increment", on_click=increment)
  slow_component()


def increment(e: me.ClickEvent):
  me.state(State).count += 1


@mel.web_component(path="./slow_component.js")
def slow_component():
  mel.insert_web_component(name="slow-component")
