---
date: 2023-12-25
---

# Hello, Mesop

After working on Mesop for the last two months, I'm excited to finally announce the first version of Mesop, v0.1. This is still early days for Mesop, but it's an important milestone because it represents a minimum viable tool for building UIs in Python. In case you haven't read Mesop's [home page](https://google.github.io/mesop/), Mesop is a Python-based UI framework that allows you to rapidly build web demos. Engineers without frontend experience can build web UIs by writing idiomatic Python code.

## Why Mesop?

Mesop is in many ways a remix of many existing ideas packaged into a single cohesive UI framework, designed for Python developers. I've documented some of these [goals](../../goals.md) previously, but I'll quickly recap the benefits of Mesop here:

- Allows non-frontend engineers to rapidly build UIs for internal use cases like demos.
- Provides a fast build-edit-refresh loop through [hot reload](../../internal/hot-reload.md).
- Enables developers to benefit from the mature [Angular](https://angular.dev/) web framework and [Angular Material](https://material.angular.io/) components.
- Provides a flexible and composable components API that's idiomatic to Python.
- Easy to deploy by using standard HTTP technologies like [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).


## What's next for Mesop?

I see a few broad themes of work in the coming year or so.

### Expand Mesop's component library

Mesop's current [component library](../../components/box.md) is a solid start but there's still gaps to support common use cases.

**Areas of work:**

- **Complete [Angular Material](https://material.angular.io/components/categories) component coverage.** We support 13+ Angular Material components today, however there's many more that we don't support. Some of it is because I haven't had time to wrap their components, but in other cases (e.g. [sidenav](https://github.com/google/mesop/issues/30)), I'd like to spend more time exploring the design space as it will probably require supporting some kind of multi-slot component API. Getting this API designed correctly, for not just this component but also future components, is important in the long run.

- **Support more native HTML elements/browser APIs.** Right now, only [Box](../../components/box.md) and [Text](../../components/text.md) are thin wrappers around native HTML elements. However, there are other HTML elements like `<img>`, `<audio>`
 and `<video>` that I'd like to also support. The flip side of supporting these components is enabling a way to allow Mesop end-users to upload these media contents, which there are also native browser APIs for.

- **Custom components.** Some components won't belong in the standard Mesop package because it's either too experimental or too use-case specific. It would be nice to have a complete story for supporting custom components. Today, all of the components use the [component helper](https://github.com/google/mesop/blob/main/mesop/component_helpers/helper.py) API which wraps internal framework details like runtime. However, there still isn't a very good story for loading custom components in the Angular frontend (e.g. ComponentRenderer's [type to component map](https://github.com/google/mesop/blob/main/mesop/web/src/component_renderer/type_to_component.ts)) and testing them.


### Make it easy to get started with Mesop

Using Mesop today requires following our [internal development setup](../../internal/development.md) which requires dependencies like Bazel/iBazel which makes it easy to interoperate with our downstream sync, but these dependencies aren't commonly used in the Python ecosystem. Eventually, I'd like make using Mesop as simple as `pip install mesop` and then using Mesop's built-in CLI: `mesop serve` for local development and `mesop deploy` to deploy on a Cloud service.

**Areas of work:**

- **Find a suitable ibazel replacement for Hot Reload.** Instead of requiring Mesop developers to sync the entire repo and building the project with Bazel and iBazel, we should distribute a ready-to-use pip package of Mesop. However, this leaves an open question of how we support [hot reload](../../internal/hot-reload.md) without iBazel which provides: 1) a filesystem watching mechanism and 2) live reload. We'll need to investigate good open-source equivalents for each of these capabilities.

- **Provide web-based interactive demos.** Many JavaScript UI frameworks provide a playground (e.g. [Angular](https://angular.dev/playground)) or interactive tutorial (e.g. [Solid](https://www.solidjs.com/tutorial/introduction_basics)) so that prospective developers can use the framework before going through the hassle of setting up their own local dev environment. This would also be very helpful to provide for each component as it's a lot easier to understand a component by tinkering with a live example.

### Explore power use cases

Today Mesop is good for internal apps with relatively un-stringent demands in terms of UI customizability and performance. For production-grade external apps, there's several areas that Mesop would need to advance in, before it's ready.

**Areas of work:**

- **Optimize network payload.** Right now the client sends the entire state to the server, and the server responds with the entire state and component tree. For large UIs/apps, this can result in sizable network payloads. We can optimize this by sending deltas as much as possible. For example, the server can send a delta of the state and component tree to the client. In addition, if we use [POST instead of GET](https://github.com/google/mesop/issues/26), we can stop using base-64 encoding which adds a significant overhead on top of Protobuf binary serialization.

- **Stateful server.** Even with the above optimizations, we'd essentially preserve the current architecture, but there's some limitations in how much improvements we can make as long as we assume servers are stateless. However, if we allow stateful servers (i.e. long-lived connections between the client and server), we can use things like WebSockets and *always* send deltas bi-directionally, in particular from client to server which isn't possible with a stateless server. The problem with this direction, though, is that it makes deployment more complex as scaling a WebSocket-based server can be hard depending on the cloud infrastructure used. In addition, we'll need to handle new edge cases like authentication and broken WebSockets connections.

- **Optimistic UI.** One of the drawbacks for server-driven UI frameworks like Mesop is that it introduces significant latency to simple user interactions. For example, if you click a button, it requires a network roundtrip before the UI is (meaningfully) updated. One way of dealing with this shortcoming is by pre-fetching the next UI state based on a user hint. For example, if a user is hovering over a button, we could optimistically calculate the state change and component tree change ahead of time before the actual click. The obvious downside to this is that optimistically executing an action is inappropriate in many cases, for example, a non-reversible action (e.g. delete) should never be optimistically done. To safely introduce this concept, we could provide an (optional) annotation for event handlers like `@me.optimistic(events=[me.HoverEvent])` so develpers could opt-in.

Some of these directions are potentially mutually exclusive. For example, having a **stateful server** may make **optimistic UI** practically more difficult because a stateful server means that non-serializable state could start to creep in to Mesop applications which makes undoing optimistic UI updates tricky

There's, of course, even more directions than what I've listed here. For example, it's technically possible to compile Python into WebAssembly and run it in the browser and this could be another way of tackling latency to user interactions. However, this seems like a longer-term exploration, which is why I've left it out for now.

## Interested in contributing?

If any of this excites you, please reach out. The easiest way is to raise a [GitHub issue](https://github.com/google/mesop/issues) and let me know if there's something specific you'd like to contribute.
