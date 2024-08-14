# Interactivity

This guide continues from the [event handlers guide](./event-handlers.md) and explains advanced interactivity patterns for dealing with common use cases such as calling a slow blocking API call or a streaming API call.

## Intermediate loading state

If you are calling a slow blocking API (e.g. several seconds) to provide a better user experience, you may want to introduce a custom loading indicator for a specific event.

> Note: Mesop has a built-in loading indicator at the top of the page for all events.

```python
--8<-- "mesop/examples/docs/loading.py"
```

In this example, our event handler is a Python generator function. Each `yield` statement yields control back to the Mesop framework and executes a render loop which results in a UI update.

Before the first yield statement, we set `is_loading` to True on state so we can show a spinner while the user is waiting for the slow API call to complete.

Before the second (and final) yield statement, we set `is_loading` to False, so we can hide the spinner and then we add the result of the API call to state so we can display that to the user.

> Tip: you must have a yield statement as the last line of a generator event handler function. Otherwise, any code after the final yield will not be executed.

## Streaming

This example builds off the previous Loading example and makes our event handler a generator function so we can incrementally update the UI.

```python
--8<-- "mesop/examples/docs/streaming.py"
```

## Async

If you want to do multiple long-running operations concurrently, then we recommend you to use Python's `async` and `await`.

```python
--8<-- "mesop/examples/async_await.py"
```

## Troubleshooting

### User input race condition

If you notice a race condition with user input (e.g. [input](../components/input.md) or [textarea](../components/textarea.md)) where sometimes the last few characters typed by the user is lost, you are probably unnecessarily setting the value of the component.

See the following example using this **anti-pattern** :warning::

```py title="Bad example: setting the value and using on_input"
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

There's several ways to fix this which are shown below.

#### Option 1: Use `on_blur` instead of `on_input`

You can use the `on_blur` event instead of `on_input` to only update the input value when the user loses focus on the input field.

This is also more performant because it sends much fewer network requests.

```py title="Good example: setting the value and using on_input"
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

#### Option 2: Do not set the input value from the server

If you don't need to set the input value from the server, then you can remove the `value` attribute from the input component.

```py title="Good example: not setting the value" hl_lines="7"
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

#### Option 3: Use two separate variables for initial and current input value

If you need set the input value from the server *and* you need to use `on_input`, then you can use two separate variables for the initial and current input value.

```py title="Good example: using two separate variables for initial and current input value" hl_lines="9"
@me.stateclass
class State:
  initial_input_value: str = "initial_value"
  current_input_value: str

@me.page()
def app():
  state = me.state(State)
  me.input(value=state.initial_input_value, on_input=on_input)

def on_input(event: me.InputEvent):
  state = me.state(State)
  state.current_input_value = event.value
```

## Next steps

Learn about layouts to build a customized UI.

<a href="../layouts" class="next-step">
    Layouts
</a>
