# Concepts

## High-level overview

Mesop is a Python library for building user interfaces. It uses a functional programming model, with inspiration from React and Redux.

The main idea of Mesop is that the UI is a pure function of state.

```
f(state) -> UI
```

## Components

Components are the building blocks of the UI. They are Python functions.

There are two kinds of components in Mesop:

1. **Native** components are built using Angular. Mesop comes with a default set of native components, but you will also be able to build your own <TODO>.
1. **Composite** components are written in Python and simple aggregate other components, including native and other composites.

Example usage of the native text component:

```python
import mesop as me

me.text("Hello, world!")
```

Example usage of creating your own composite component:

```python
import mesop as me

def my_composite():
    me.text("Hello")
    me.text("World")
```

This will render "Hello" and "World" in two consecutive lines.

## Interactivity

When a user interacts with the UI, an action is triggered. This action is processed by a **handler** which is a function that takes the current state and event and updates the state.

```
f(state, event) -> None
```

Here's a simple example showing interactivity:

```python
from dataclasses import dataclass
import mesop as me

@dataclass
class State:
    text: str

store = me.store(
    State(text="initial_state"),
)

@me.on(me.CheckboxEvent)
def checkbox_change(state: State, event: me.CheckboxEvent):
    if event.checked:
        state.text = "checked"
    else:
        state.text = "unchecked
    return state

def my_composite():
    state = store.get_state()
    me.checkbox(label="Check?" on_change=checkbox_change)
    me.text(state.text)
```

## Slow / async work

Oftentimes, you will need to do some heavy-processing, for example waiting for a blocking API call to run an ML model or streaming back incremental responses to the user.

### Streaming response

If you are building a chat-style LLM application, you will oftentimes want to stream the response so that users can see something before waiting for the entire response to complete.

```python
import mesop as me

@me.on(me.ClickEvent)
def chat(state: State, action: me.ClickEvent):
    response = streaming_api_call(...)
    for chunk in response:
        state.text += chunk.text
        yield state

def main():
    me.button("Start chat", on_click=chat)
```

### Loading indicator

If you're calling a heavy API which doesn't support streaming, you may instead want to show a loading indicator so that users know the system is working.

```python
import mesop as me

@me.on(me.ClickEvent)
def chat(state: State, action: me.ClickEvent):
    state.in_progress = True
    yield state
    response = blocking_api_call(...)
    state.in_progress = False
    state.response = response
    yield state

def main():
    me.button("Start chat", on_click=chat)
```

## Tips

- Component are expected to be fast and pure functions. If you need to update state, you should trigger an action handle it in a handler.
