import json
from dataclasses import asdict, dataclass, field, is_dataclass
from io import StringIO
from typing import Any, Type, TypeVar, cast, get_origin, get_type_hints

from mesop.exceptions import MesopException

_PANDAS_OBJECT_KEY = "__pandas.DataFrame__"

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
      elif get_origin(type_hint) == dict:
        setattr(cls, name, field(default_factory=dict))
      elif isinstance(type_hint, type):
        setattr(
          cls, name, field(default_factory=dataclass_with_defaults(type_hint))
        )

  return dataclass(cls)


def serialize_dataclass(state: Any):
  if is_dataclass(state):
    json_str = json.dumps(asdict(state), cls=MesopJSONEncoder)
    return json_str
  else:
    raise MesopException("Tried to serialize state which was not a dataclass")


def update_dataclass_from_json(instance: Any, json_string: str):
  data = json.loads(json_string, object_hook=decode_mesop_json_state_hook)
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


class MesopJSONEncoder(json.JSONEncoder):
  """
  Custom JSON Encoder to handle special serialization cases.

  Since we support Pandas DataFrames in the Mesop table, users may need to store the
  the DataFrames in Mesop State. This means we need a way to serialize the DataFrame to
  JSON and back.

  For simplicity we will convert the DataFrame to JSON within the JSON serialized state.
  This makes it so we don't have to worry about serializing other data types used by
  Pandas. The "table" serialization format is verbose, but will ensure the most accurate
  deserialization back into a DataFrame.
  """

  def default(self, obj):
    try:
      import pandas as pd

      if isinstance(obj, pd.DataFrame):
        return {_PANDAS_OBJECT_KEY: pd.DataFrame.to_json(obj, orient="table")}
    except ImportError:
      pass
    return super().default(obj)


def decode_mesop_json_state_hook(dct):
  """
  Object hook to decode JSON for Mesop state.

  Since we support Pandas DataFrames in the Mesop table, users may need to store the
  the DataFrames in Mesop State. This means we need a way to serialize the DataFrame to
  JSON and back.

  One thing to note is that pandas.NA becomes numpy.nan during deserialization.
  """
  try:
    import pandas as pd

    if _PANDAS_OBJECT_KEY in dct:
      return pd.read_json(StringIO(dct[_PANDAS_OBJECT_KEY]), orient="table")
  except ImportError:
    pass
  return dct
