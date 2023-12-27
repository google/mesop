import json
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Type, TypeVar, cast, get_origin, get_type_hints

from mesop.exceptions import MesopException

C = TypeVar("C")


def dataclass_with_defaults(cls: Type[C]) -> Type[C]:
  """
  Provides defaults for every attribute in a dataclass (recursively) so
  Mesop developers don't need to manually set default values
  """
  pass
  annotations = get_type_hints(cls)
  for name, type_hint in annotations.items():
    if name not in cls.__dict__:  # Skip if default already set
      if type_hint == int:
        setattr(cls, name, field(default=0))
      elif type_hint == float:
        setattr(cls, name, field(default=0.0))
      elif type_hint == str:
        setattr(cls, name, field(default=""))
      elif type_hint == bool:
        setattr(cls, name, field(default=False))
      elif get_origin(type_hint) == list:
        setattr(cls, name, field(default_factory=list))
      elif isinstance(type_hint, type):
        setattr(
          cls, name, field(default_factory=dataclass_with_defaults(type_hint))
        )

  return dataclass(cls)


def serialize_dataclass(state: Any):
  if is_dataclass(state):
    json_str = json.dumps(asdict(state))
    return json_str
  else:
    raise MesopException("Tried to serialize state which was not a dataclass")


def update_dataclass_from_json(instance: Any, json_string: str):
  data = json.loads(json_string)
  _recursive_update_dataclass_from_json_obj(instance, data)


def _recursive_update_dataclass_from_json_obj(instance: Any, json_dict: Any):
  for key, value in json_dict.items():
    if hasattr(instance, key):
      attr = getattr(instance, key)
      if isinstance(value, dict):
        # If the value is a dict, recursively update the dataclass.
        setattr(
          instance,
          key,
          _recursive_update_dataclass_from_json_obj(attr, value),
        )
      elif isinstance(value, list):
        updated_list: list[Any] = []
        for item in cast(list[Any], value):
          if isinstance(item, dict):
            # If the json item value is an instance of dict,
            # we assume it should be converted into a dataclass
            attr = getattr(instance, key)
            item_instance = instance.__annotations__[key].__args__[0]()
            updated_list.append(
              _recursive_update_dataclass_from_json_obj(item_instance, item)
            )
          else:
            # If the item is not a dict, append it directly.
            updated_list.append(item)
        setattr(instance, key, updated_list)
      else:
        # For other types, set the value directly.
        setattr(instance, key, value)
  return instance
