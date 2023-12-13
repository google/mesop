import json
from dataclasses import fields
from typing import Any


def clear_dataclass(instance: Any):
  for field in fields(instance):
    setattr(instance, field.name, field.default)


def update_dataclass_from_json(instance: Any, json_string: str):
  print("updating dataclass from json", instance, json_string)
  clear_dataclass(instance)  # Clear the instance first
  data = json.loads(json_string)
  for key, value in data.items():
    if hasattr(instance, key):
      setattr(instance, key, value)
