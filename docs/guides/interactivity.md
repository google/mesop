# Interactivity

This guide continues from the Counter app example in [Getting Started](../getting_started.md#counter-app) and explains advanced interactivity patterns.

## State

Example state class:

```python
@me.stateclass
class State:
  clicks: int
```

Each user session, which is equivalent to a browser session, will have its own state instance. Everything in a state class, recursively, must be serializable. This is because, under the hood, Mesop is sending the state back and forth between the server and browser client.

### Nested State

You can also have classes inside of a state class as long as everything is serializable:

```python
class NestedState:
  val: int

@me.stateclass
class State:
  nested: NestedState

def app():
  state = me.state(State)
```

> Note: you only need to decorate the top-level state class with `@me.stateclass`. All the nested state classes will automatically be wrapped.

## Slow / async patterns

These are patterns for dealing with common use cases such as calling a slow blocking API call or a streaming API call.

### Loading

If you are calling a slow blocking API (e.g. several seconds) to provide a better user experience, you may want to introduce a custom loading indicator for a specific event.

> Note: Mesop has a built-in loading indicator at the top of the page for all events.

```python
--8<-- "mesop/examples/docs/loading.py"
```

In this example, our event handler is a Python generator function. Each `yield` statement yields control back to the Mesop framework and executes a render loop which results in a UI update.

Before the first yield statement, we set `is_loading` to True on state so we can show a spinner while the user is waiting for the slow API call to complete.

Before the second (and final) yield statement, we set `is_loading` to False, so we can hide the spinner and then we add the result of the API call to state so we can display that to the user.

> Tip: you must have a yield statement as the last line of a generator event handler function. Otherwise, any code after the final yield will not be executed.

### Streaming

This example builds off the previous Loading example and makes our event handler a generator function so we can incrementally update the UI.

```python
--8<-- "mesop/examples/docs/streaming.py"
```
