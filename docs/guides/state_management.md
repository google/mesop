# State Management

State management is a critical element of building interactive apps because it allows you store information about what the user did in a structured way.

## Basic usage

You can register a class using the class decorator `me.stateclass` which is like a dataclass with special powers:

```python
@me.stateclass
class State:
  val: str
```

You can get an instance of the state class inside any of your Mesop component functions by using `me.state`:

```py
@me.page()
def page():
    state = me.state(State)
    me.text(state.val)
```

## Use immutable default values

Similar to [regular dataclasses which disallow mutable default values](https://docs.python.org/3/library/dataclasses.html#mutable-default-values), you need to avoid mutable default values such as list and dict for state classes. Using mutable default values can result in leaking state across sessions which can be a serious privacy issue.

You **MUST** use immutable default values _or_ use dataclasses `field` initializer _or_ not set a default value.

???+ success "Good: immutable default value"
      Setting a default value to an immutable type like str is OK.

      ```py
      @me.stateclass
      class State:
        a: str = "abc"
      ```

???+ failure "Bad: mutable default value"

    This will raise an exception because dataclasses prevents you from using mutable collection types like `list` as the default value because this is a common footgun.

    ```py
    @me.stateclass
    class State:
      a: list[str] = ["abc"]
    ```

???+ success "Good: default factory"

    If you want to set a field to a mutable default value, use default_factory in the `field`  function from the dataclasses module to create a new instance of the mutable default value for each instance of the state class.

    ```py
    from dataclasses import field

    @me.stateclass
    class State:
      a: list[str] = field(default_factory=lambda: ["abc"])
    ```

???+ success "Good example of no default value"

    If you want a default of an empty list, you can just not define a default value and Mesop will automatically define an empty list default value.

    For example, if you write the following:

    ```py
    @me.stateclass
    class State:
      a: list[str]
    ```

    It's the equivalent of:

    ```py
    @me.stateclass
    class State:
      a: list[str] = field(default_factory=list)
    ```

## How State Works

`me.stateclass` is a class decorator which tells Mesop that this class can be retrieved using the `me.state` method, which will return the state instance for the current user session.

> If you are familiar with the dependency injection pattern, Mesop's stateclass and state API is essentially a minimalist dependency injection system which scopes the state object to the lifetime of a user session.

Under the hood, Mesop is sending the state back and forth between the server and browser client so everything in a state class must be serializable.

## Multiple state classes

You can use multiple classes to store state for the current user session.

Using different state classes for different pages or components can help make your app easier to maintain and more modular.

```py
@me.stateclass
class PageAState:
    ...

@me.stateclass
class PageBState:
    ...

@me.page(path="/a")
def page_a():
    state = me.state(PageAState)
    ...

@me.page(path="/b")
def page_b():
    state = me.state(PageBState)
    ...
```

Under the hood, Mesop is managing state classes based on the identity (e.g. module name and class name) of the state class, which means that you could have two state classes named "State", but if they are in different modules, then they will be treated as separate state, which is what you would expect.

## Nested State

You can also have classes inside of a state class as long as everything is serializable:

```python
class NestedState:
  val: str

@me.stateclass
class State:
  nested: NestedState

def app():
  state = me.state(State)
```

> Note: you only need to decorate the top-level state class with `@me.stateclass`. All the nested state classes will automatically be wrapped.

### Nested State and dataclass

Sometimes, you may want to explicitly decorate the nested state class with `dataclass` because in the previous example, you couldn't directly instantiate `NestedState`.

If you wanted to use NestedState as a general dataclass, you can do the following:

```python
@dataclass
class NestedState:
  val: str = ""

@me.stateclass
class State:
  nested: NestedState

def app():
  state = me.state(State)
```

> Reminder: because dataclasses do not have default values, you will need to explicitly set default values, otherwise Mesop will not be able to instantiate an empty version of the class.

Now, if you have an event handler function, you can do the following:

```py
def on_click(e):
    response = call_api()
    state = me.state(State)
    state.nested = NestedState(val=response.text)
```

If you didn't explicitly annotate NestedState as a dataclass, then you would get an error instantiating NestedState because there's no initializer defined.

## Tips

### State performance issues

Because the state class is serialized and sent back and forth between the client and server, you should try to keep the state class reasonably sized. For example, if you store a very large string (e.g. base64-encoded image) in state, then it will degrade performance of your Mesop app. Instead, you should try to store large data outside of the state class (e.g. in-memory, filesystem, database, external service) and retrieve the data as needed for rendering.

#### Storing state in memory

Mesop has a feature that allows you to store state in memory rather than passing the
full state on every request. This may help improve performance when dealing with large
state objects. The caveat is that storing state in memory contains its own set of
problems that you must carefully consider. See the [config section](../api/config.md#mesop_state_session_backend)
for details on how to use this feature.
