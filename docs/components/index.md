# Components

Please read [Core Concepts](../getting-started/core-concepts.md) before this as it explains the basics of components. This page provides an overview of the different types of components in Mesop.

## Types of components

### Native components

Native components are components implemented using Angular/Javascript. Many of these components wrap [Angular Material components](https://material.angular.io/components/). Other components are simple wrappers around DOM elements.

If you have a use case that's not supported by the existing native components, please [file an issue on GitHub](https://github.com/google/mesop/issues/new) to explain your use case. Given our limited bandwidth, we may not be able to build it soon, but in the future, we will enable Mesop developers to build their own custom native components.

### User-defined components

User-defined components are essentially Python functions which call other components, which can be native components or other user-defined components. It's very easy to write your own components, and it's encouraged to split your app into modular components for better maintainability and reusability.

### Web components

Web components in Mesop are custom HTML elements created using JavaScript and CSS. They enable custom JavaScript execution and bi-directional communication between the browser and server. They can wrap JavaScript libraries and provide stateful client-side interactions. [Learn more about web components](../web-components/index.md).

## Content components

Content components allow you to compose components more flexibly than regular components by accepting child(ren) components. A commonly used content component is the [button](./button.md) component, which accepts a child component which oftentimes the [text](./text.md) component.

Example:

```python
with me.button():
  me.text("Child")
```

You can also have multiple content components nested:

```python
with me.box():
  with me.box():
    me.text("Grand-child")
```

Sometimes, you may want to define your own content component for better reusability. For example, let's say I want to define a scaffold component which includes a menu positioned on the left and a main content area, I could do the following:

```python
@me.content_component
def scaffold(url: str):
  with me.box(style=me.Style(background="white")):
    menu(url=url)
    with me.box(style=me.Style(padding=me.Padding(left=MENU_WIDTH))):
      me.slot()
```

Now other components can re-use this scaffold component:

```python
def page1():
  with scaffold(url="/page1"):
    some_content(...)
```

This is similar to Angular's [Content Projection](https://angular.io/guide/content-projection).

## Component Key

Every native component in Mesop accepts a `key` argument which is a component identifier. This is used by Mesop to tell [Angular whether to reuse the DOM element](https://angular.io/api/core/TrackByFunction#description).

### Resetting a component

You can reset a component to the initial state (e.g. reset a [select](./select.md) component to the unselected state) by giving it a new key value across renders.

For example, you can reset a component by "incrementing" the key:

```py
class State:
  select_menu_key: int

def reset(event):
  state = me.state(State)
  state.select_menu_key += 1

def main():
  state = me.state(State)
  me.select(key=str(state.select_menu_key),
            options=[me.SelectOption(label="o1", value="o1")])
  me.button(label="Reset", on_click=reset)
```

### Event handlers

Every Mesop event includes the key of the component which emitted the event. This makes it useful when you want to reuse an event handler for multiple instances of a component:

```py
def buttons():
  for fruit in ["Apple", "Banana"]:
    me.button(fruit, key=fruit, on_click=on_click)

def on_click(event: me.ClickEvent):
  fruit = event.key
  print("fruit name", fruit)
```

Because a key is a `str` type, you may sometimes want to store more complex data like a dataclass or a proto object for retrieval in the event handler. To do this, you can serialize and deserialize:

```py
import json
from dataclasses import dataclass

@dataclass
class Person:
  name: str

def buttons():
  for person in [Person(name="Alice"), Person(name="Bob")]:
    # serialize dataclass into str
    key = json.dumps(person.asdict())
    me.button(person.name, key=key, on_click=on_click)

def on_click(event: me.ClickEvent):
  person_dict = json.loads(event.key)
  # modify this for more complex deserialization
  person = Person(**person_dict)
```

!!! Tip "Use component key for reusable event handler"

    This avoids a [subtle issue with using closure variables in event handlers](../guides/interactivity.md#avoid-using-closure-variables-in-event-handler).
