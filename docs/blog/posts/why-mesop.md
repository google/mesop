---
date: 2024-05-13
hide:
  - toc
---

# Why Mesop?

Mesop is a new UI framework that enables Python developers to quickly build delightful web apps in a scalable way.

Many Python UI frameworks are easy to get started with, but customizing beyond the defaults often requires diving into JavaScript, CSS, and HTML — a steep learning curve for many developers.

Mesop provides a different approach, offering a framework that's both easy to learn and enables flexible UI building, all within Python.

I want to share a couple concrete ways in which Mesop achieves this.

## Build UIs with Functions (i.e. Components)

Mesop embraces a component-based philosophy where the entire UI is composed of reusable, building blocks which are called components. Using a component is as simple as calling a Python function. This approach offers several benefits:

- **Simplicity:** You can use your existing Python knowledge to build UIs quickly and intuitively since components are just functions.
- **Maintainability:** Complex UIs become easier to manage and understand by breaking them down into smaller, focused components.
- **Modularity:** Components are self-contained, enabling easy reuse within a project or across different projects.

Here's an example of a reusable icon button component:

```python
def icon_button(*, icon: str, label: str, tooltip: str, on_click: Callable):
  """Icon button with text and tooltip."""
  with me.content_button(on_click=on_click):
    with me.tooltip(message=tooltip):
      with me.box(style=me.Style(display="flex")):
        me.icon(icon=icon)
        me.text(
          label, style=me.Style(line_height="24px", margin=me.Margin(left=5))
        )

```

## Flexibility through Layered Building Blocks

Mesop provides a range of UI building blocks, from low-level [native components](https://google.github.io/mesop/components/#native-components) to high-level components.

- Low-level components: like [box](../../components/box.md), offer granular control over layout and styling. They empower you to create custom UI elements through flexible layouts like flexbox and grid.
- High-level components: like [chat](../../components/chat.md), are built from low-level components and provide ready-to-use elements for common use cases, enabling rapid development.

This layered approach makes deep customization possible. This means that if you want to customize the chat component, you can fork the [chat implementation](https://github.com/google/mesop/blob/main/mesop/labs/chat.py) because it's written entirely in Python using Mesop's public APIs.

## See Mesop in Action

To demonstrate the range of UIs possible with Mesop, we built a demo gallery to showcase the types of applications you can build and the components that are available:

<iframe class="immersive-demo" src="https://google.github.io/mesop/demo/"></iframe>

 The [demo gallery](https://mesop-y677hytkra-uc.a.run.app/) itself is a Mesop app and [implemented](https://github.com/google/mesop/blob/d0b3e286d0dd9de49eb1d5e3bbc1ab84e96a6d08/demo/main.py) in a few hundred lines of Python code. It demonstrates how Mesop can be used to create polished, custom UIs in a maintainable way.

## Try Mesop

If this sounds intriguing, read the [Getting Started guide](../../getting-started/installing.md) and try building your own Mesop app. [Share your feedback and contribute](https://github.com/google/mesop/issues) as we continue developing Mesop.
