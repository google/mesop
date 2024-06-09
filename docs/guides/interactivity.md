# Interactivity

This guide continues from the Counter app example in [Quickstart](../getting_started/quickstart.md#counter-app) and explains advanced interactivity patterns for dealing with common use cases such as calling a slow blocking API call or a streaming API call.

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

## Troubleshooting

### User input race condition

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

### Avoid using closure variables in event handler

One subtle mistake when building a reusable component is to have the event handler use a closure variable like the following example:

```py title="Bad example of using closure variable"
@me.component
def link_component(url: str):
   def on_click(event: me.ClickEvent):
     me.navigate(url)
  return me.button(url, on_click=on_click)

def app():
    link_component("/1")
    link_component("/2")
```

The problem with this above example is that Mesop only stores the last event handler. This means that both instances of the link_component will refer to the last `on_click` instance which references the same `url` closure variable set to `"/2"`. This almost always produces the wrong behavior.

Instead, you will want to use the pattern of relying on the key in the event handler as demonstrated in the following example:

```py title="Good example of using key"
@me.component
def link_component(url: str):
   def on_click(event: me.ClickEvent):
     me.navigate(event.key)
  return me.button(url, key=url, on_click=on_click)
```

For more info on using component keys, please refer to the [Component Key docs](./components.md#component-key).
