import hashlib
import inspect
from functools import wraps
from typing import Any, Callable, Generator, Type, TypeVar, cast, overload

from google.protobuf import json_format
from google.protobuf.message import Message

import mesop.protos.ui_pb2 as pb
from mesop.component_helpers.style import Style, to_style_proto
from mesop.events import ClickEvent, InputEvent, MesopEvent
from mesop.exceptions import MesopDeveloperException
from mesop.key import Key, key_from_proto
from mesop.runtime import runtime
from mesop.utils.caller import get_caller_source_code_location
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


def slot():
  runtime().context().save_current_node_as_slot()


class _UserCompositeComponent:
  def __init__(self, fn: Callable[..., Any]):
    self.prev_current_node = runtime().context().current_node()
    fn()
    node_slot = runtime().context().node_slot()
    node_slot_children_count = runtime().context().node_slot_children_count()
    if not node_slot or node_slot_children_count is None:
      raise MesopDeveloperException(
        "Must configure a child slot when defining a composite component."
      )
    runtime().context().set_current_node(node_slot)
    # Temporarily remove children that are after the slot
    self.after_children = node_slot.children[node_slot_children_count:]
    for child in self.after_children:
      node_slot.children.remove(child)

  def __enter__(self):
    pass

  def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
    # Re-add the children temporarily removed in __init__
    for child in self.after_children:
      insert = runtime().context().current_node().children.add()
      insert.MergeFrom(child)
    runtime().context().set_current_node(self.prev_current_node)


def content_component(fn: Callable[..., Any]):
  @wraps(fn)
  def wrapper(*args: Any, **kwargs: Any):
    return _UserCompositeComponent(lambda: fn(*args, **kwargs))

  return wrapper


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
        source_code_location = get_caller_source_code_location(levels=2)
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
    source_code_location = get_caller_source_code_location(levels=7)
  return _ComponentWithChildren(
    type_name=type_name,
    proto=proto,
    key=key,
    style=to_style_proto(style) if style else None,
    source_code_location=source_code_location,
  )


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
    source_code_location = get_caller_source_code_location(levels=7)
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

  wrapper.__module__ = func.__module__
  wrapper.__name__ = func.__name__

  return wrapper


def register_event_handler(
  handler_fn: Callable[..., Any], event: Type[Any]
) -> str:
  fn_id = compute_fn_id(handler_fn)

  runtime().context().register_event_handler(
    fn_id, wrap_handler_with_event(handler_fn, event)
  )
  return fn_id


def compute_fn_id(fn: Callable[..., Any]) -> str:
  source_code = inspect.getsource(fn)
  # Skip hashing the fn/module name in debug mode because it makes it hard to debug.
  if runtime().debug_mode:
    source_code_hash = hashlib.sha256(source_code.encode()).hexdigest()
    return f"{fn.__module__}.{fn.__name__}.{source_code_hash}"
  input = f"{fn.__module__}.{fn.__name__}.{source_code}"
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
  ),
)

runtime().register_event_mapper(
  InputEvent,
  lambda userEvent, key: InputEvent(
    value=userEvent.string_value,
    key=key.key,
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
