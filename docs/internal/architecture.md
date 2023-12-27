# Architecture

This doc is meant to provide an overview of how Mesop is structured as a framework. It's not necessary to know this information as a developer using Mesop, but if you're _developing_ Mesop's codebase, then this is helpful in laying out the lay of the land.

At the heart of Mesop is two subsystems:

- A Python server, running on top of [Flask](https://flask.palletsprojects.com/en/).
- A Web client, built on [Angular](https://angular.dev/) framework, which wraps various [Angular components](https://angular.dev/guide/components), particularly [Angular Material components](https://material.angular.io/components/).

## Terminology

- *Downstream* - This refers to the synced version of Mesop inside of Google (["google3 third-party"](https://opensource.google/documentation/reference/thirdparty)). Although almost all the code is shared between the open-source and internal version of Mesop, there's many considerations in maintaining parity between these two versions, particularly with regards to [toolchain](./toolchain.md).
- *Component* vs *component instance* - A component typically refers to the Python factory function that creates a component instance (e.g. `me.box()`). A component instance refers to a specific component created by a component function and is represented as a `Component` proto. Other UI frameworks oftentimes give a different name for an instance (i.e. Element) of a component, but for simplicity and explicitness, I will refer to these instances as component instance or _component tree_ (for the entire tree of component instances) in this doc.

## Life of a Mesop request

### Initial page load

When a user visits a Mesop application, the following happens:

1. The user visits a path on the Mesop application, e.g. "/" (root path), in their browser.
1. The Mesop client-side web application (Angular) is bootstrapped and sends an `InitRequest` to the server.
1. The Mesop server responds with a `RenderEvent` which contains a fully instantiated component tree.
1. The Mesop client renders the component tree. Every Mesop component instance corresponds to 1 or more Angular component instance.

### User interactions

If the user interacts with the Mesop application (e.g. click a button), the following happens:

1. The user triggers a `UserEvent` which is sent to the server. The UserEvent includes: the application state (represented by the `States` proto), the event handler id to trigger, the key of the component interacted with (if any), and the payload value (e.g. for checkbox, it's a bool value which represents the checked state of the checkbox).
1. The server does the following:
    1. Runs a first render loop in tracing mode (i.e. instantiate the component tree from the root component of the requested path). This discovers any event handler functions. In the future, this trace can also be used to calculate the before component tree so we can calculate the diff of the component tree to minimize the network payload.
    1. Updates the state by feeding the user event to the event handler function discovered in the previous step.
    > Note: there's a mapping layer between the UserEvent proto and the granular Python event type. This provides a nicer API for Mesop developers then the internal proto representation.
    1. Runs a second render loop to generate the new component tree given the new state. After the first render loop, each render loop results in a RenderEvent sent to the client.
    1. In the [streaming](../guides/interactivity.md#streaming) case, we may run the render loop and flush it down via [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) many times.
1. The client re-renders the Angular application after receiving each RenderEvent.

## Python Server

Flask is a minimalist Python server framework that conforms to WSGI ([Web Server Gateway Interface](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)), which is a Python standard that makes it easy for web servers (oftentimes written in other languages like C++) to delegate requests to a Python web framework. This is particularly important in the downstream case because we rely on an internal HTTP server to serve Mesop applications.

For development purposes (i.e. using the CLI), we use [Werkzeug](https://werkzeug.palletsprojects.com/en/), which is a WSGI library included with Flask.

## Web Client

Mesop's Web client consists of three main parts:

- **Core**: Includes the root Angular component and singleton services like `Channel`. This part is fairly small and is the critical glue between the rest of the client layer and the server.
- **Mesop Components**: Every Mesop component has its own directory under `/components`
> Note: this includes both the Python API and the Angular implementation for developer convenience.
- **Dev Tools**: Mesop also comes with a basic set of developer tools, namely the components and log panels. The components panel allows Mesop developers to visualize the component tree. The log panel allows Mesop developers to inspect the application state and component tree values.

## Static assets

- Using the regular CLI, the web client static assets (i.e. JS binary, CSS, images) are served from the Python server. This simplifies deployment of Mesop applications by reducing version skew issues between the client and server.
- In uncompiled mode (using the dev CLI), the web client is served from the web devserver. This is convenient because it builds faster than the regular/compiled mode and it allows live-reloading when developing the client codebase.

## Tooling

Outside of the `mesop/` directory are various tools used to build, test and document the Mesop framework. However, anything needed to actually run a Mesop application should be located within `mesop/`. The three main tools inside the codebase are:

- **Build tooling** - these are in `build_defs/` which contains various Bazel `bzl` files and `tools` which is forked from the Angular codebase. The build toolchain is described in more detail on the [toolchain doc](./toolchain.md).
- **Component generator** - inside `generator/` is a mini-library and CLI tool to generate Mesop components from existing Angular components, specifically Angular Material, although with some modifications it could support more generic Angular components. The generator modifies the codebase so that nothing in `generator/` is actually needed when running a Mesop applications.
- **Docs** - Mesop's doc site is built using [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/) and is what you are looking at right now.
