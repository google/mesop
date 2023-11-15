# New Component

## Steps

1. Define the Python API by creating a new file in `//optic/components/{component_name}.py`
1. Define the protos sent from server to client.
1. Define the client Angular component.
1. Update Angular `component_renderer` to load component.

## API Guidelines

- Make all arguments keyword only by putting `*` as the initial argument. Keyword argument is more readable, particularly for UI components which will have increasingly more optional arguments over time.
- **Model after existing APIs.** For example, if we are wrapping an existing @angular/material component, we will try to mirror their API (within reason). If we are wrapping a native HTML element, we should try to expose a similar API. In some cases, we will look at other UI frameworks like Flutter for inspiration, even though we are not directly wrapping them.
- **Prefer small components**. We should try to provide small native components that can be composed by composite components in Python. This enables a wider range of use cases.

## New events

Try to reuse the existing events when possible, but you may need to sometimes create a new event.

1. Define the event class in `//optic/events/{event_name}.py`
1. In the same file, define an event mapper and register it: `runtime.register_event(EventClass, event_mapper)`

## Potential exploration areas

- Consider co-locating web and Python code for a component together.
  - Would still need to register the web component in Angular.
- Have each component define its own standalone proto file. Nothing outside of the client and Python component files can access this internal data representation.
- Code-gen `component_renderer` using a shell/Python script. Initially, just run the script as-needed, but eventually can run it as part of a BUILD rule (a la [@angular/components examples](https://github.com/angular/components/tree/13629b0cd814ccc5fa01cf670b8b3001bc0021ff/tools/example-module))
- Create a converter from Python to proto?
