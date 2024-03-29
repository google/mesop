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

## Avoid using closure variables in event handler

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
