# Quickstart

> Note: Web components are a new experimental feature released under labs and may have breaking changes.

You will learn how to build your first web component step-by-step, a counter component.

Although it's a simple example, it will show you the core APIs of defining your own web component and how to support bi-directional communication between the Python code running on the server and JavaScript code running on the browser.

### Python module

Let's first take a look at the Python module which defines the interface so that the rest of your Mesop app can call the web component in a Pythonic way.

```python title="counter_component.py"
--8<-- "mesop/examples/web_component/quickstart/counter_component.py"
```

The first part you will notice is the decorator: `@mel.web_component`. This annotates a function as a web component and specifies where the corresponding JavaScript module is located, relative to the location of this Python module.

We've defined the function parameters just like a regular Python function.

> Tip: We recommend annotating your parameter with types because Mesop will do runtime validation which will catch type issues earlier.

Finally, we call the function `mel.insert_web_component` with the following arguments:

- `name` - This is the web component name and must match the name defined in the JavaScript module.
- `key` - Like all components, web components accept a key which is a unique identifier. See the [component key docs](../components/index.md#component-key) for more info.
- `events` - A dictionary where the key is the event name. This must match a property name, defined in JavaScript. The value is the event handler (callback) function.
- `properties` - A dictionary where the key is the property name that's defined in JavaScript and the value is the property value which is plumbed to the JavaScript component.

> Note: Keys for events and properties must not be "src", "srcdoc", or start with "on" to avoid web security risks.

In summary, when you see a string literal, it should match something on the JavaScript side which is explained next.

### JavaScript module

Let's now take a look at how we implement in the web component in JavaScript:

```javascript title="counter_component.js"
--8<-- "mesop/examples/web_component/quickstart/counter_component.js"
```

In this example, we have used [Lit](https://lit.dev/) which is a small library built on top of web standards in a simple, secure and declarative manner.

> Note: you can write your web components using any web technologies (e.g. TypeScript) or frameworks as long as they conform to the interface defined by your Python module.

#### Properties

The static property named `properties` defines two kinds of properties:

- **Regular properties** - these were defined in the `properties` argument of `insert_web_component`. The property name in JS must match one of the `properties` dictionary key. You also should make sure the Python and JS types are compatible to avoid issues.
- **Event properties** - these were defined in the `events` argument of `insert_web_component`. The property name in JS must match one of the `events` dictionary key. Event properties are always type `String` because the value is a handler id which identifies the Python event handler function.

#### Triggering an event

To trigger an event in your component, let's look at the `_onDecrement` method implementation:

```javascript
this.dispatchEvent(
  new MesopEvent(this.decrementEvent, {
    value: this.value - 1,
  }),
);
```

`this.dispatchEvent` is a [standard web API](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/dispatchEvent) where a DOM element can emit an event. For Mesop web components, we will always emit a `MesopEvent` which is a class provided on the global object (`window`). The first argument is the event handler id so Mesop knows which Python function to call as the event handler and the second argument is the payload which is a JSON-serializable value (oftentimes an object) that the Python event handler can access.

#### Learn more about Lit

I didn't cover the `render` function which is a [standard Lit method](https://lit.dev/docs/components/rendering/). I recommend reading through [Lit's docs](https://lit.dev/docs/getting-started/) which are excellent ahd have interactive tutorials.

### Using the component

Finally, let's use the web component we defined. When you click on the decrement button, the value will decrease from 10 to 9 and so on.

```python title="counter_component_app.py"
--8<-- "mesop/examples/web_component/quickstart/counter_component_app.py"
```

Even though this was a toy example, you've learned how to build a web component from scratch which does bi-directional communication between the Python server and JavaScript client.

## Next steps

To learn more, read the [API docs](./api.md) or look at the [examples](https://github.com/google/mesop/tree/main/mesop/examples/web_component/).
