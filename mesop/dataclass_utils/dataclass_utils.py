import json
from dataclasses import asdict, is_dataclass
from typing import Any

from mesop.exceptions import MesopException


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
      if isinstance(value, dict):
        setattr(
          instance,
          key,
          _recursive_update_dataclass_from_json_obj(
            getattr(instance, key), value
          ),
        )
      else:
        setattr(instance, key, value)
  return instance
