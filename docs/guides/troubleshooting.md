# Troubleshooting

## State must be serializable

All the fields, recursively, in your State class must be serializable.

## User input race condition

If you notice a race condition with user input (e.g. [input](../components/input.md) or [textarea](../components/textarea.md)) where sometimes the last few characters typed by the user is lost, you are probably unnecessarily setting the value of the component.

See the following example using this **anti-pattern** :warning::

```py title="Bad example"
@me.stateclass
class State:
  input_value: str

def app():
  state = me.state(State)
  me.input(value=state.input_value, on_input=on_input)

def on_input(event: me.InputEvent):
  state = me.state(State)
  state.input_value = event.value
```

The problem is that the input value now has a race condition because it's being set by two sources:

1. The server is setting the input value based on state.
2. The client is setting the input value based on what the user is typing.

The way to fix this is by *not* setting the input value from the server.

The above example **corrected** would look like this :white_check_mark::

```py title="Good example" hl_lines="7"
@me.stateclass
class State:
  input_value: str

def app():
  state = me.state(State)
  me.input(on_input=on_input)

def on_input(event: me.InputEvent):
  state = me.state(State)
  state.input_value = event.value
```
