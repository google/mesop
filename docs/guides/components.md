# Components

Please read [Getting Started](../getting_started.md) before this as it explains the basics of components. This page provides an in-depth explanation of the different types of components in Mesop.

## Kinds of components

### Native components

Native components are components implemented using Angular/Javascript. Many of these components wrap [Angular Material components](https://material.angular.io/components/). Other components are simple wrappers around DOM elements.

If you have a use case that's not supported by the existing native components, please [file an issue on GitHub](https://github.com/google/mesop/issues/new) to explain your use case. Given our limited bandwidth, we may not be able to build it soon, but in the future, we will enable Mesop developers to build their own custom native components.

### User-defined components

User-defined components are essentially Python functions which call other components, which can be native components or other user-defined components. It's very easy to write your own components, and it's encouraged to split your app into modular components for better maintainability and reusability.

## Composite components

Composite components allow you to compose components more flexibly than regular components. A commonly used composite component is the [button](../components/button.md) component, which accepts a child component which oftentimes the [text](../components/text.md) component.

Example:

```python
with me.button():
  me.text("Child")
```

You can also have multiple composite components nested:

```python
with me.box():
  with me.box():
    me.text("Grand-child")
```

Sometimes, you may want to define your own composite component for better reusability. For example, let's say I want to define a scaffold component which includes a menu positioned on the left and a main content area, I could do the following:

```python
@me.composite
def scaffold(url: str):
  with me.box(style="background: white"):
    menu(url=url)
    with me.box(style=f"padding-left: {MENU_WIDTH}px"):
      me.slot()
```

Now other components can re-use this scaffold component:

```python
def page1():
  with scaffold(url="/page1"):
    some_content(...)
```

This is similar to Angular's [Content Projection](https://angular.io/guide/content-projection).
