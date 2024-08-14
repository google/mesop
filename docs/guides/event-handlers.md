# Event Handlers

Event handlers are a core part of Mesop and enables you to handle user interactions by writing Python functions which are called by the Mesop framework when a user event is received.

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

Because Mesop has a stateless architecture, we need a way of computing an id for the event handler function that's stable across Python runtimes. For example, the initial page may be rendered by one Python server, but another server may be used to respond to the user event. This stateless architecture allows Mesop apps to be fault-tolerant and enables simple scaling.

## Types of event handlers

### Regular functions

These are the simplest and most common type of event handlers used. It's essentially a regular Python function which is called by the Mesop framework when a user event is received.

```py title="Regular function"
def on_click(event: me.ClickEvent):
    state = me.state(State)
    state.count += 1
```

### Generator functions

Python Generator functions are a powerful tool, which allow you to `yield` multiple times in a single event handler. This allows you to render intermediate UI states.

```py title="Generator function"
def on_click(event: me.ClickEvent):
    state = me.state(State)
    state.count += 1
    yield
    time.sleep(1)
    state.count += 1
    yield
```

You can learn more about real-world use cases of the generator functions in the [Interactivity guide](./interactivity.md).

???+ info "Always yield at the end of a generator function"
    If you use a `yield` statement in your event handler, then the event handler will be a generator function. You must have a `yield` statement at the end of the event handler (or each return point), otherwise not all of your code will be executed.

### Async generator functions

Python async generator functions allow you to do concurrent work using Python's `async` and `await` language features. If you are using async Python libraries, you can use these types of event handlers.

```py title="Async generator function"
async def on_click(event: me.ClickEvent):
    state = me.state(State)
    state.count += 1
    yield
    await asyncio.sleep(1)
    state.count += 1
    yield
```

For a more complete example, please refer to the [Async section of the Interactivity guide](./interactivity.md#async).

???+ info "Always yield at the end of an async generator function"
    Similar to a regular generator function, an async generator function must have a `yield` statement at the end of the event handler (or each return point), otherwise not all of your code will be executed.

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

If you want to reuse event handler logic between generator functions, you can use the [`yield from`](https://docs.python.org/3/whatsnew/3.3.html#pep-380) syntax. For example, let's say `call_api` in the above example is a generator function. You can use `yield from` to reuse the event handler logic:

```py title="Reusing event handler logic for generator functions"
def on_enter(event: me.InputEnterEvent):
    state = me.state(State)
    state.value = event.value
    yield from call_api()

def on_click(event: me.ClickEvent):
    yield from call_api()

def call_api():
    # Do initial work
    yield
    # Do more work
    yield
```
### Boilerplate-free event handlers

If you're building a form-like UI, it can be tedious to write a separate event handler for each form field. Instead, you can use this pattern which utilizes the `key` attribute that's available in most events and uses Python's built-in `setattr` function to dynamically update the state:

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

The downside of this approach is that you lose type safety. Generally, defining a separate event handler, although more verbose, is easier to maintain.

## Troubleshooting

### Avoid using closure variables in event handler

One subtle mistake when building a reusable component is having the event handler use a closure variable, as shown in the following example:

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

The problem with this above example is that Mesop only stores the last event handler. This is because each event handler has the same id which means that Mesop cannot differentiate between the two instances of the same event handler.

This means that both instances of the link_component will refer to the last `on_click` instance which references the same `url` closure variable set to `"/2"`. This almost always produces the wrong behavior.

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
