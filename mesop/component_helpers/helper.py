import hashlib
import inspect
import json
from dataclasses import dataclass, is_dataclass
from dataclasses import field as dataclass_field
from enum import Enum
from functools import lru_cache, partial, wraps
from typing import (
  Any,
  Callable,
  Generator,
  Generic,
  KeysView,
  ParamSpec,
  Type,
  TypeVar,
  cast,
  get_type_hints,
  overload,
)

from google.protobuf import json_format
from google.protobuf.message import Message

import mesop.protos.ui_pb2 as pb
from mesop.component_helpers.style import Style, to_style_proto
from mesop.events import ClickEvent, InputEvent, MesopEvent, WebEvent
from mesop.exceptions import MesopDeveloperException
from mesop.key import Key, key_from_proto
from mesop.runtime import runtime
from mesop.runtime.context import NodeSlot, NodeTreeState
from mesop.utils.caller import (
  get_app_caller_source_code_location,
)
from mesop.utils.validate import validate


class _ComponentWithChildren:
  def __init__(
    self,
    type_name: str,
    proto: Message,
    key: str | None = None,
    style: pb.Style | None = None,
    source_code_location: pb.SourceCodeLocation | None = None,
  ):
    self.prev_current_node = runtime().context().current_node()
    self.component = self.prev_current_node.children.add()
    self.component.MergeFrom(
      create_component(
        component_name=pb.ComponentName(core_module=True, fn_name=type_name),
        proto=proto,
        key=key,
        style=style,
        source_code_location=source_code_location,
      )
    )

  def __enter__(self):
    runtime().context().set_current_node(self.component)

  def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
    runtime().context().set_current_node(self.prev_current_node)


def slot(name: str = ""):
  """
  This function is used when defining a content component to mark a place in the component tree where content
  can be provided by a child component.

  Args:
    name: A name can be specified for named slots. Multiple named slots in a composite component must use unique names.
  """
  runtime().context().save_current_node_as_slot(name)


S = TypeVar("S")
T = TypeVar("T")
P = ParamSpec("P")


class NamedSlot:
  def __init__(self, node_tree_state: NodeTreeState, name: str = ""):
    self.is_accessed = False
    self.name = name
    self.node_tree_state = node_tree_state

  def __call__(self):
    if self.is_accessed:
      raise MesopDeveloperException(
        f"Content for named slot '{self.name}' has already been set."
      )
    self.is_accessed = True
    return DetachedNodeTreeStateContext(self.node_tree_state)


def slotclass(cls: type[S]) -> type[S]:
  """Restricted dataclass that enforces that all fields are NamedSlot type."""
  for attr, expected_type in get_type_hints(cls).items():
    if expected_type is not NamedSlot:
      raise MesopDeveloperException(
        f"Slotclass field '{attr}` must be of type 'me.NamedSlot'"
      )
  return dataclass(kw_only=True)(cls)


@slotclass
class UnnamedSlot:
  pass


@dataclass(kw_only=True)
class SlotMetadata:
  """Metadata for slot.

  Attributes:
    node_slot: Position of the slot.
    node_tree_state: Detached node tree state for this slot.
  """

  node_slot: NodeSlot
  node_tree_state: NodeTreeState = dataclass_field(
    default_factory=NodeTreeState
  )


class DetachedNodeTreeStateContext:
  """Context helper for tracing a component sub tree with detached node state.

  This is needed for processing the sub trees of multiple slots within
  a composite component.
  """

  def __init__(self, node_tree_state: NodeTreeState):
    self.prev_node_tree_state = runtime().context().get_node_tree_state()
    runtime().context().set_node_tree_state(node_tree_state)

  def __enter__(self):
    pass

  def __exit__(self, exc_type, exc_val, exc_tb):
    runtime().context().set_node_tree_state(self.prev_node_tree_state)


class _UserCompositeComponent(Generic[S]):
  def __init__(self, fn: Callable[[], Any], named_slots_cls: type[S]):
    self.prev_current_node = runtime().context().current_node()
    node_tree_state = runtime().context().get_node_tree_state()
    self.prev_node_tree_state = node_tree_state
    # Add a null slot which acts as a bookmark for slots added by this composite
    # component.
    node_tree_state.add_null_slot()
    fn()

    self.unnamed_slot = None
    self.named_slots = {}

    if named_slots_cls is UnnamedSlot:
      if len(node_tree_state.node_slots()) != 1:
        raise MesopDeveloperException(
          "Must configure one child slot when defining a content component with unnamed slots."
        )
      if node_tree_state.node_slots()[0].name:
        raise MesopDeveloperException(
          "Named slots are not allowed when defining a content component with unnamed slots."
        )
      self.unnamed_slot = SlotMetadata(
        node_slot=node_tree_state.node_slots()[0]
      )
      DetachedNodeTreeStateContext(self.unnamed_slot.node_tree_state)
    else:
      self.named_slots = {
        node_slot.name: SlotMetadata(node_slot=node_slot)
        for node_slot in node_tree_state.node_slots()
      }

      if len(self.named_slots) != len(node_tree_state.node_slots()):
        raise MesopDeveloperException(
          "Multiple slots of the same name encountered. The names must be unique within the content component."
        )

    self.slot_context = named_slots_cls(
      **{
        named_slot: NamedSlot(
          slot_metadata.node_tree_state, slot_metadata.node_slot.name
        )
        for named_slot, slot_metadata in self.named_slots.items()
      }
    )

  def __enter__(self) -> S:
    return self.slot_context

  def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
    if self.unnamed_slot:
      self._insert_slot_content(self.unnamed_slot)

    # Need to insert named slots in reversed order to preserve the correct insertion
    # indexes. Insertion order is preserved in dicts in 3.7+
    for slot_name in reversed(self.named_slots):
      if not getattr(self.slot_context, slot_name).is_accessed:
        raise MesopDeveloperException(
          f"Content for named slot '{slot_name}' was not set."
        )
      self._insert_slot_content(self.named_slots[slot_name])

    # Reset node tree back to previous position to continue traversal.
    runtime().context().set_node_tree_state(self.prev_node_tree_state)
    runtime().context().set_current_node(self.prev_current_node)
    runtime().context().clear_node_slots_to_first_null_slot()

  def _insert_slot_content(self, slot_metadata: SlotMetadata) -> None:
    index = slot_metadata.node_slot.insertion_index
    parent_node = slot_metadata.node_slot.parent_node
    current_items = list(parent_node.children)
    current_items[index:index] = (
      slot_metadata.node_tree_state.current_node().children
    )
    del parent_node.children[:]
    for item in current_items:
      parent_node.children.add().CopyFrom(item)


# Overload when the decorator is called with parens, e.g.
# @content_component(named_slots=ExampleNamedSlots)
# def fn():
@overload
def content_component(
  *,
  named_slots: type[S],
) -> Callable[[Callable[P, Any]], Callable[P, _UserCompositeComponent[S]]]:
  pass


# Overload when the decorator is called without parens, e.g.
# @content_component
# def fn():
@overload
def content_component(
  decorated_fn: Callable[P, Any] | None = None,
  /,
) -> Callable[P, _UserCompositeComponent[UnnamedSlot]]:
  pass


def content_component(
  decorated_fn: Callable[P, Any] | None = None,
  /,
  *,
  named_slots: type[S] | None = None,
):
  def named_content_component_wrapper(
    fn: Callable[P, Any],
    /,
  ) -> Callable[P, _UserCompositeComponent[S]]:
    @wraps(fn)
    def wrapper(
      *args: P.args, **kwargs: P.kwargs
    ) -> _UserCompositeComponent[S]:
      if named_slots:
        return _UserCompositeComponent(
          lambda: fn(*args, **kwargs), named_slots_cls=named_slots
        )
      else:
        # This exception should never be called since `named_content_component_wrapper`
        # should only be called with the first overload, which requires the `named_slot`
        # parameter.
        raise MesopDeveloperException("No slotclass provided.")

    return cast(Callable[P, _UserCompositeComponent[S]], wrapper)

  # Separate function is used for the unnamed case since we need to explicitly pass in
  # the `UnnamedSlot`. VSCode type checking gets confused when using Unions in
  # `_UserCompositeComponent` (e.g. def __enter__(self) -> S | UnnamedSlot). It can't
  # seem to determine when S is used or when UnnamedSlot is used.
  def content_component_wrapper(
    fn: Callable[P, Any],
    /,
  ) -> Callable[P, _UserCompositeComponent[UnnamedSlot]]:
    @wraps(fn)
    def wrapper(
      *args: P.args, **kwargs: P.kwargs
    ) -> _UserCompositeComponent[UnnamedSlot]:
      return _UserCompositeComponent(
        lambda: fn(*args, **kwargs), named_slots_cls=UnnamedSlot
      )

    return cast(Callable[P, _UserCompositeComponent[UnnamedSlot]], wrapper)

  if decorated_fn is None:
    return named_content_component_wrapper

  return content_component_wrapper(decorated_fn)


C = TypeVar("C", bound=Callable[..., Any])


# Overload when the decorator is called without parens, e.g.
# @component
# def fn():
@overload
def component(
  decorated_fn: C | None = None,
  /,
) -> C:
  pass


# Overload when the decorator is called with parens, e.g.
# @component(skip_validation=True)
# def fn():
@overload
def component(
  *,
  skip_validation: bool = False,
) -> Callable[[C], C]:
  pass


def component(
  decorated_fn: Callable[..., Any] | None = None,
  /,
  *,
  skip_validation: bool = False,
):
  def component_wrapper(fn: C) -> C:
    """Wraps a Python function to make it a user-defined component."""

    validated_fn = fn if skip_validation else validate(fn)

    @wraps(fn)
    def wrapper(*args: Any, **kw_args: Any):
      prev_current_node = runtime().context().current_node()
      component = prev_current_node.children.add()
      source_code_location = None
      if runtime().debug_mode:
        source_code_location = get_app_caller_source_code_location()
      component.MergeFrom(
        create_component(
          component_name=get_component_name(fn),
          proto=pb.UserDefinedType(
            args=[
              pb.UserDefinedType.Arg(
                arg_name=kw_arg, code_value=map_code_value(value)
              )
              for kw_arg, value in kw_args.items()
              if map_code_value(value) is not None
            ]
          ),
          source_code_location=source_code_location,
        )
      )
      runtime().context().set_current_node(component)
      ret = validated_fn(*args, **kw_args)
      runtime().context().set_current_node(prev_current_node)
      return ret

    runtime().register_native_component_fn(fn)
    return cast(C, wrapper)

  if decorated_fn is None:
    return component_wrapper
  else:
    return component_wrapper(decorated_fn)


def get_component_name(fn: Callable[..., Any]) -> pb.ComponentName:
  if "mesop.components" in fn.__module__:
    return pb.ComponentName(core_module=True, fn_name=fn.__name__)
  return pb.ComponentName(fn_name=fn.__name__, module_path=fn.__module__)


def map_code_value(value: Any) -> pb.CodeValue | None:
  if isinstance(value, str):
    return pb.CodeValue(string_value=value)
  if isinstance(value, int):
    return pb.CodeValue(int_value=value)
  if isinstance(value, float):
    return pb.CodeValue(double_value=value)
  if isinstance(value, bool):
    return pb.CodeValue(bool_value=value)
  return None


def create_component(
  component_name: pb.ComponentName,
  proto: Message,
  key: str | None = None,
  style: pb.Style | None = None,
  source_code_location: pb.SourceCodeLocation | None = None,
) -> pb.Component:
  type_index = 0
  # This is not exactly type-safe, but it's a convenient way of grabbing the
  # type index value.
  if hasattr(proto, "type_index"):
    type_index = proto.type_index  # type: ignore
  type = pb.Type(
    name=component_name,
    value=proto.SerializeToString(),
    type_index=type_index,  # type: ignore
  )
  style_debug_json = ""
  if runtime().debug_mode:
    type.debug_json = json_format.MessageToJson(
      proto, preserving_proto_field_name=True
    )
    if style:
      style_debug_json = json_format.MessageToJson(
        style, preserving_proto_field_name=True
      )

  return pb.Component(
    key=pb.Key(key=key),
    type=type,
    style=style,
    style_debug_json=style_debug_json,
    source_code_location=source_code_location,
  )


def insert_composite_component(
  type_name: str,
  proto: Message,
  key: str | None = None,
  style: Style | None = None,
) -> _ComponentWithChildren:
  source_code_location = None
  if runtime().debug_mode:
    source_code_location = get_app_caller_source_code_location()
  return _ComponentWithChildren(
    type_name=type_name,
    proto=proto,
    key=key,
    style=to_style_proto(style) if style else None,
    source_code_location=source_code_location,
  )


class _WebComponentWithSlots(Generic[S]):
  def __init__(
    self,
    *,
    type_proto: pb.WebComponentType,
    key: str | None,
    name: str,
    named_slots_cls: type[S],
  ):
    """A context manager that creates a <web> component plus named slots."""

    self.type_proto = type_proto
    self.key = key
    self.component_name = "<web>" + name
    self.named_slots_cls = named_slots_cls

    self.prev_node: pb.Component | None = None
    self.created_component: pb.Component | None = None

    # We will store {slot_name: SlotMetadata}, and then in __enter__
    # we fill it in, once we know the parent node for sure.
    self.named_slot_metadata: dict[str, SlotMetadata] = {}

    # The user’s “slots” dataclass instance – we create it in __enter__.
    self.slots_dataclass_instance: S | None = None

  def __enter__(self) -> S:
    # Insert the web component now
    self.prev_node = runtime().context().current_node()

    # Create the node for the <web> component
    #   (like what insert_composite_component(...) does, but
    #    we inline it here so we can hold a reference to it.)
    source_code_location = None
    if runtime().debug_mode:
      source_code_location = get_app_caller_source_code_location()

    parent_node = self.prev_node
    self.created_component = parent_node.children.add()
    self.created_component.MergeFrom(
      create_component(
        component_name=pb.ComponentName(
          core_module=True, fn_name=self.component_name
        ),
        proto=self.type_proto,
        key=self.key,
        style=None,
        source_code_location=source_code_location,
      )
    )

    # Now, for each field in named_slots_cls, create a “detached” NodeTreeState.
    # Then we build a NamedSlot object that, when called, sets the context to that sub‐tree.
    # We'll store them in self.named_slot_metadata.

    # We also need a separate NodeTreeState for each slot. The easiest approach is:
    # 1) For each field in the dataclass -> create a NodeTreeState + NamedSlot
    # 2) Build a "SlotMetadata" that we can splice in at __exit__ time.
    #    We'll store them in self.named_slot_metadata[slot_name].

    slot_fields = get_type_hints(self.named_slots_cls).keys()
    for field_name in slot_fields:
      # Each field in the user’s named slots dataclass is a NamedSlot (enforced by @slotclass).
      node_tree_state = NodeTreeState()
      slot_meta = SlotMetadata(
        node_slot=NodeSlot(
          parent_node=self.created_component,  # We'll eventually put children here
          insertion_index=0,  # We'll compute final insertion order in __exit__
          name=field_name,
        ),
        node_tree_state=node_tree_state,
      )
      self.named_slot_metadata[field_name] = slot_meta

    # Now build the user’s actual dataclass instance, passing NamedSlot(...) for each field.
    # The NamedSlot constructor wants (node_tree_state, name).
    # That object is what the user uses as “s.header()”, etc.

    # Note: We'll preserve the order in slot_fields.  But in Python 3.7+,
    # get_type_hints should preserve definition order for a standard dataclass.
    # If not, you could also rely on <dataclass>.__dataclass_fields__.

    slot_kwargs = {}
    for field_name, slot_meta in self.named_slot_metadata.items():
      slot_kwargs[field_name] = NamedSlot(
        node_tree_state=slot_meta.node_tree_state,
        name=slot_meta.node_slot.name,
      )

    # Instantiate user’s slot dataclass
    self.slots_dataclass_instance = self.named_slots_cls(**slot_kwargs)

    # Return the user’s slots dataclass, so they can do `with s.header(): ...`
    return self.slots_dataclass_instance

  def __exit__(self, exc_type, exc_val, exc_tb):
    # Now we splice the sub-trees for each named slot into the web component's children.

    # We'll track a running insertion index so the slots appear
    # in the same order as the dataclass fields (or any order you like).
    insertion_index = 0
    for field_name in self.named_slot_metadata:
      slot_meta = self.named_slot_metadata[field_name]
      # Splice the children from slot_meta.node_tree_state into the web node
      slot_children = slot_meta.node_tree_state.current_node().children

      # Convert to a list so we can do insertion easily
      current_children = list(self.created_component.children)
      # Insert the new children at insertion_index
      current_children[insertion_index:insertion_index] = slot_children
      insertion_index += len(slot_children)

      # Clear out the old children
      del self.created_component.children[:]
      # Copy them back
      for child in current_children:
        self.created_component.children.add().CopyFrom(child)

    # Switch back to old node context
    if self.prev_node is not None:
      runtime().context().set_current_node(self.prev_node)

    # If you need to remove "extra" node slots from the context,
    # you might do `runtime().context().clear_node_slots_to_first_null_slot()`
    # or something else. Typically you do that for nested @content_component use.

    self.slots_dataclass_instance = None


def insert_web_component(
  *,
  name: str,
  events: dict[str, Callable[[WebEvent], Any] | None] | None = None,
  properties: dict[str, Any] | None = None,
  key: str | None = None,
  named_slots: type[S] | None = None,
):
  """
  Inserts a web component into the current component tree. If 'named_slots' is not
  provided, it simply inserts and returns None.

  If 'named_slots' is provided, it returns a context-manager object (like a
  content component), so the user can do:

     with insert_web_component(..., named_slots=MySlots) as slots:
         with slots.header():
             ...
         with slots.body():
             ...

  Then, once the with-block ends, we finalize the sub-trees.
  """
  if events is None:
    events = {}
  if properties is None:
    properties = {}

  filtered_events = filter_web_events(events)
  check_property_keys_is_safe(filtered_events.keys())
  check_property_keys_is_safe(properties.keys())

  # register event handlers
  event_to_ids: dict[str, str] = {}
  for event, handler in filtered_events.items():
    event_to_ids[event] = register_event_handler(handler, WebEvent)

  type_proto = pb.WebComponentType(
    properties_json=json.dumps(properties),
    events_json=json.dumps(event_to_ids),
  )

  # If user didn't provide named_slots, just do immediate insertion
  if named_slots is None:
    # This is the original pattern
    return insert_composite_component(
      type_name="<web>" + name,
      proto=type_proto,
      key=key,
      style=None,
    )

  # Otherwise, return our new WebComponentWithSlots manager
  return _WebComponentWithSlots(
    type_proto=type_proto,
    key=key,
    name=name,
    named_slots_cls=named_slots,
  )


def filter_web_events(
  events: dict[str, Callable[[WebEvent], Any] | None],
) -> dict[str, Callable[[WebEvent], Any]]:
  """Helper function for filtering out web component events that do not have a callback."""
  return {event: callback for event, callback in events.items() if callback}


# Note: the logic here should be kept in sync with
# component_renderer.ts's checkAttributeNameIsSafe
#
# We check here in Python to provide a better error message and
# developer experience.
def check_property_keys_is_safe(keys: KeysView[str]):
  """
  Follow web security best practices by ensuring dangerous attributes
  aren't used by raising an exception.
  """
  for key in keys:
    # Lowercase the key because DOM attributes are case insensitive
    normalized_key = key.lower()
    # https://security.stackexchange.com/a/139861
    if normalized_key in ["src", "srcdoc"] or normalized_key.startswith("on"):
      raise MesopDeveloperException(
        f"Cannot use '{key}' as a key for insert_web_component events or properties because this can cause web security issues."
      )


# TODO: remove insert_custom_component
def insert_custom_component(
  component_name: str,
  proto: Message,
  key: str | None = None,
  style: Style | None = None,
):
  return insert_component(
    # Prefix with <custom> to ensure there's never any overlap.
    type_name="<custom>" + component_name,
    proto=proto,
    key=key,
    style=style,
  )


def insert_component(
  type_name: str,
  proto: Message,
  key: str | None = None,
  style: Style | None = None,
) -> None:
  """
  Inserts a component into the current context's current node.
  """
  source_code_location = None
  if runtime().debug_mode:
    source_code_location = get_app_caller_source_code_location()
  runtime().context().current_node().children.append(
    create_component(
      component_name=pb.ComponentName(core_module=True, fn_name=type_name),
      proto=proto,
      key=key,
      style=to_style_proto(style) if style else None,
      source_code_location=source_code_location,
    )
  )


E = TypeVar("E", bound=MesopEvent)
Handler = Callable[[E], None | Generator[None, None, None]]


def wrap_handler_with_event(func: Handler[E], actionType: Type[E]):
  def wrapper(action: E):
    # This is guaranteed to be a UserEvent because only Mesop
    # framework will call the wrapper.
    proto_event = cast(pb.UserEvent, action)
    key = key_from_proto(proto_event.key)

    event = runtime().get_event_mapper(actionType)(proto_event, key)

    return func(cast(Any, event))

  if isinstance(func, partial):
    wrapper.__module__ = func.func.__module__
    wrapper.__name__ = func.func.__name__
  else:
    wrapper.__module__ = func.__module__
    wrapper.__name__ = func.__name__

  return wrapper


def register_event_handler(
  handler_fn: Callable[..., Any], event: Type[E]
) -> str:
  fn_id = compute_fn_id(handler_fn)

  runtime().context().register_event_handler(
    fn_id, wrap_handler_with_event(handler_fn, event)
  )
  return fn_id


def has_stable_repr(obj: Any) -> bool:
  """Check if an object has a stable repr.
  We need to ensure that the repr is stable between different Python runtimes.
  """
  stable_types = (int, float, str, bool, type(None), tuple, frozenset, Enum)  # type: ignore

  if isinstance(obj, stable_types):
    return True
  if is_dataclass(obj):
    return all(
      has_stable_repr(getattr(obj, f.name))
      for f in obj.__dataclass_fields__.values()
    )
  if isinstance(obj, (list, set)):
    return all(has_stable_repr(item) for item in obj)  # type: ignore
  if isinstance(obj, dict):
    return all(
      has_stable_repr(k) and has_stable_repr(v)
      for k, v in obj.items()  # type: ignore
    )

  return False


@lru_cache(maxsize=None)
def compute_fn_id(fn: Callable[..., Any]) -> str:
  if isinstance(fn, partial):
    func_source = inspect.getsource(fn.func)
    # For partial functions, we need to ensure that the arguments have a stable repr
    # because we use the repr to compute the fn_id.
    for arg in fn.args:
      if not has_stable_repr(arg):
        raise MesopDeveloperException(
          f"Argument {arg} for functools.partial event handler {fn.func.__name__} does not have a stable repr"
        )

    for k, v in fn.keywords.items():
      if not has_stable_repr(v):
        raise MesopDeveloperException(
          f"Keyword argument {k}={v} for functools.partial event handler {fn.func.__name__} does not have a stable repr"
        )

    args_str = ", ".join(repr(arg) for arg in fn.args)
    kwargs_str = ", ".join(f"{k}={v!r}" for k, v in fn.keywords.items())
    partial_args = (
      f"{args_str}{', ' if args_str and kwargs_str else ''}{kwargs_str}"
    )

    source_code = f"partial(<<{func_source}>>, {partial_args})"
    fn_name = fn.func.__name__
    fn_module = fn.func.__module__
  else:
    source_code = inspect.getsource(fn) if inspect.isfunction(fn) else str(fn)
    fn_name = fn.__name__
    fn_module = fn.__module__

  # Skip hashing the fn/module name in debug mode because it makes it hard to debug.
  if runtime().debug_mode:
    source_code_hash = hashlib.sha256(source_code.encode()).hexdigest()
    return f"{fn_module}.{fn_name}.{source_code_hash}"
  input = f"{fn_module}.{fn_name}.{source_code}"
  return hashlib.sha256(input.encode()).hexdigest()


def get_qualified_fn_name(fn: Callable[..., Any]) -> str:
  return f"{fn.__module__}.{fn.__name__}"


def register_native_component(fn: C) -> C:
  """Registers the component with runtime to provide editor support
  (e.g. suggestion for new component).

  Returns a component function which validates arguments.
  """
  runtime().register_native_component_fn(fn)
  return validate(fn)


def register_event_mapper(
  event: Type[E], map_fn: Callable[[pb.UserEvent, Key], E]
):
  runtime().register_event_mapper(event=event, map_fn=map_fn)


runtime().register_event_mapper(
  ClickEvent,
  lambda userEvent, key: ClickEvent(
    key=key.key,
    is_target=userEvent.click.is_target,
  ),
)


runtime().register_event_mapper(
  InputEvent,
  lambda userEvent, key: InputEvent(
    value=userEvent.string_value,
    key=key.key,
  ),
)

runtime().register_event_mapper(
  WebEvent,
  lambda userEvent, key: WebEvent(
    key=key.key,
    value=json.loads(userEvent.string_value),
  ),
)


_COMPONENT_DIFF_FIELDS = (
  "key",
  "source_code_location",
  "style",
  "style_debug_json",
  "type",
)


def diff_component(
  component1: pb.Component, component2: pb.Component
) -> pb.ComponentDiff:
  """Finds diffs between two component trees.

  Args:
    component1: Old version of the component tree.
    component2: New version of the component tree that we want component1 to match.

  Returns:
    Changes needed to make component1 equal to component2.
  """
  diff = pb.ComponentDiff()

  # Check each field for differences. For now if there are any differences, we will
  # mark the entire field for replacement.
  for field in _COMPONENT_DIFF_FIELDS:
    if getattr(component1, field) != getattr(component2, field):
      diff.diff_type = pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE
      setattr(
        diff,
        f"update_strategy_{field}",
        pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
      )
      if isinstance(getattr(component2, field), Message):
        getattr(diff, field).CopyFrom(getattr(component2, field))
      else:
        setattr(diff, field, getattr(component2, field))

  # Handle differences with child components.
  for index, child_component in enumerate(component1.children):
    if index >= len(component2.children):
      diff.diff_type = pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE
      diff.children.append(
        pb.ComponentDiff(
          index=index, diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_DELETE
        )
      )
    else:
      child_diff = diff_component(child_component, component2.children[index])
      if (
        child_diff
        and child_diff.diff_type != pb.ComponentDiff.DiffType.DIFF_TYPE_NONE
      ):
        diff.diff_type = pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE
        child_diff.index = index
        diff.children.append(child_diff)

  # Find child components that do not exist in component 1. These will need to be added
  # to component 1.
  #
  # It is also very important that the add component diffs occur after the
  # delete diffs since that additions would mess up the deletions.
  #
  # Although in practice child components diffs can contain either add or delete
  # operations, but not both.
  for index, component2_child in enumerate(component2.children):
    if index >= len(component1.children):
      diff.diff_type = pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE
      diff.children.append(
        pb.ComponentDiff(
          index=index,
          diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
          component=component2_child,
        )
      )

  return diff
