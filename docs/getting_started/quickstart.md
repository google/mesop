# Quickstart

Let's build a simple interactive Mesop app.

## Before you start

Make sure you've installed Mesop, otherwise please follow the [Installing Guide](./installing.md).

## Text to text app

The simplest way to get started with Mesop is to use the [`text_to_text` component](../components/text_to_text.md)

```python
--8<-- "mesop/examples/text_to_text.py"
```

The rest of this guide will show you step-by-step how something like text_to_text is implemented.

## Hello World app

Let's start by creating a simple Hello World app in Mesop:

```python
--8<-- "mesop/examples/docs/hello_world.py"
```

This simple example demonstrates a few things:

- Every Mesop app starts with `import mesop as me`. This is the only recommended way to import mesop, otherwise your app may break in the future because you may be relying on internal implementation details.
- `@me.page` is a function decorator which makes a function a _root component_ for a particular path. If you omit the `path` parameter, this is the equivalent of doing `@me.page(path="/")`.
- `app` is a Python function that we will call a __component__ because it's creating Mesop components in the body.

## Components

Components are the building blocks of a Mesop application. A Mesop application is essentially a tree of components.

Let's explain the different kinds of components in Mesop:

- Mesop comes built-in with __native__ components. These are components implemented using Angular/Javascript. Many of these components wrap [Angular Material components](https://material.angular.io/components/).
- You can also create your own components which are called __user-defined__ components. These are essentially Python functions like `app` in the previous example.

## Counter app

Let's build a more complex app to demonstrate Mesop's interactivity features.

```python
--8<-- "mesop/examples/docs/counter.py"
```

This app allows the user to click on a button and increment a counter, which is shown to the user as "Clicks: #".

Let's walk through this step-by-step.

### State

The `State` class represents the application state for a particular browser session. This means every user session has its own instance of `State`.

`@me.stateclass` is a class decorator which is similar to Python's [dataclass](https://docs.python.org/3/library/dataclasses.html) but also sets default value based on type hints and allows Mesop to inject the class as shown next.

> Note: Everything in a state class must be serializable because it's sent between the server and browser.

### Event handler

The `button_click` function is an event handler. An event handler has a single parameter, `event`, which can contain a value (this will be shown in the next example). An event handler is responsible for updating state based on the incoming event.

`me.state(State)` retrieves the instance of the state class for the current session.

### Component

Like the previous example, `main` is a Mesop component function which is decorated with `page` to mark it as a root component for a path.

Similar to the event handler, we can retrieve the state in a component function by calling `me.state(State)`.

> Note: it's _not_ safe to mutate state inside a component function. All mutations must be done in an event handler.

Rendering dynamic values in Mesop is simple because you can do standard Python string interpolation use f-strings:

```python
me.text(f"Clicks: {state.clicks}")
```

The button component demonstrates two aspects of calling a Mesop component:

```python
with me.button(on_click=button_click):
  me.text("Increment")
```

The `with` statement allows you to nest components inside another component. In this case, we want to show the text "Increment", so we call `me.text` as a child component inside of `me.button`.

The `on_click` argument is how you wire the event handler defined above to a specific component. Whenever a click event is triggered by the component, the registered event handler function is called.

In summary, you've learned how to define a state class, an event handler and wire them together using interactive components.

## What's next

At this point, you've learned all the basics of building a Mesop app and now you should be able to understand how [Text to Text is implemented](https://github.com/google/mesop/blob/main/mesop/labs/text_to_text.py) under the hood.

To learn more about Mesop, I recommend reading the [Guides](../guides/components.md) and then spend time looking at the [examples on GitHub](https://github.com/google/mesop/tree/main/mesop/examples). As you build your own applications, you'll want to reference the [Components API reference](../components/button.md) docs.
