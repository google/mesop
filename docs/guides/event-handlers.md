# Event Handlers

Event handlers are a core part of Mesop and enables you to handle user interactions by writing Python functions (callbacks).

## How it works

Let's take a look at a simple example of an event handler:

```py title="Simple event handler"
def counter():
    me.button("Increment", on_click=on_click)

def on_click(event: me.ClickEvent):
    state = me.state(State)
    state.count += 1

@me.stateclass
class State:
    count: int = 0
```

Although this example looks simple, there's a lot going on under the hood.

When the counter function is called, it creates an instance of the button component and binds the `on_click` event handler to it. Because components (and the entire Mesop UI) is serialized and sent to the client, we need a way of serializing the event handler so that when the button is clicked, the correct event handler is called on the server.

We don't actually need to serialize the entire event handler, rather we just need to compute a unique id for the event handler function.

Because Mesop has a stateless architecture, we need a way of computing an id for the event handler function that's stable across Python runtimes. For example, the initial page made be rendered by one Python server, but another server may be used to respond to the user event. This stateless architecture allows Mesop apps to be fault tolerant and allows for easy scaling of the app.

## Patterns

### Reusing event handler logic

You can share event handler logic by extracting the common logic into a separate function. For example, you will often want to use the same logic for the `on_enter` event handler for an input component and the `on_click` event handler for a "send" button component.

```py title="Reusing event handler logic"
def on_enter(event: me.InputEnterEvent):
    state = me.state(State)
    state.value = event.value
    call_api()

def on_click(event: me.ClickEvent):
    # Assumes that state.value has been set by an on_blur event handler
    call_api()

def call_api():
    # Put your common event handler logic here
    pass
```

### Boilerplate-free event handlers

If you're building a form-like UI, it can be tedious to write a separate event handler for each form field. Instead, you can use this pattern:

```py title="Boilerplate-free event handlers"
def app():
  me.input(label="Name", key="name", on_blur=update_state)
  me.input(label="Address", key="address", on_blur=update_state)

@me.stateclass
class State:
  name: str
  address: str

def update_state(event: me.InputBlurEvent):
  state = me.state(State)
  setattr(state, event.key, event.value)
```

The downside with this approach is that you lose type-safety. Generally, defining a separate event handler, although more verbose, is easier to maintain.

## Troubleshooting

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

For more info on using component keys, please refer to the [Component Key docs](../components/index.md#component-key).

## Next steps

Explore advanced interactivity patterns like streaming and async:

<a href="../interactivity" class="next-step">
    Interactivity
</a>
