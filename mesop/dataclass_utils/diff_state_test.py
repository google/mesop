import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd
import pytest

from mesop.components.uploader.uploaded_file import UploadedFile
from mesop.dataclass_utils.dataclass_utils import diff_state
from mesop.exceptions import MesopException


def test_no_diff():
  @dataclass
  class C:
    val1: str = "val1"

  assert json.loads(diff_state(C(), C())) == []


def test_diff_primitives():
  @dataclass
  class C:
    val1: str = "val1"
    val2: int = 1
    val3: float = 1.1
    val4: bool = True
    val5: Optional[bool] = True

  s1 = C()
  s2 = C(val1="VAL1", val2=2, val3=1.2, val4=False, val5=None)

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["val5"],
      "action": "type_changes",
      "value": None,
      "type": "<class 'NoneType'>",
      "old_type": "<class 'bool'>",
    },
    {"path": ["val1"], "action": "values_changed", "value": "VAL1"},
    {"path": ["val2"], "action": "values_changed", "value": 2},
    {"path": ["val3"], "action": "values_changed", "value": 1.2},
    {"path": ["val4"], "action": "values_changed", "value": False},
  ]


def test_diff_core_data_structures():
  @dataclass
  class C:
    val1: list[int] = field(default_factory=lambda: [1, 2, 3])
    val2: dict[str, str] = field(default_factory=lambda: {"k1": "v1"})
    val3: tuple[str, str] = field(default_factory=lambda: ("t1", "t2"))

  s1 = C()
  s2 = C(val1=[2, 3, 4], val2={"k2": "v2"}, val3=("t2", "t1"))

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val2", "k2"], "value": "v2", "action": "dictionary_item_added"},
    {
      "path": ["val2", "k1"],
      "value": "v1",
      "action": "dictionary_item_removed",
    },
    {"path": ["val3", 0], "action": "values_changed", "value": "t2"},
    {"path": ["val3", 1], "action": "values_changed", "value": "t1"},
    {"path": ["val1", 2], "value": 4, "action": "iterable_item_added"},
    {"path": ["val1", 0], "value": 1, "action": "iterable_item_removed"},
  ]


def test_diff_nested_dataclass():
  @dataclass
  class B:
    val1: int = 1

  @dataclass
  class C:
    val1: B

  s1 = C(val1=B())
  s2 = C(val1=B(val1=2))

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", "val1"], "action": "values_changed", "value": 2}
  ]


def test_diff_nested_class():
  class B:
    def __init__(self, val1: int = 1):
      self.val1 = val1

  @dataclass
  class C:
    val1: B

  s1 = C(val1=B())
  s2 = C(val1=B(val1=2))
  print(json.loads(diff_state(s1, s2)))
  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", "val1"], "action": "values_changed", "value": 2}
  ]


def test_diff_type_change():
  @dataclass
  class C:
    val1: str | bool = "String"

  s1 = C()
  s2 = C(val1=True)
  print(json.loads(diff_state(s1, s2)))
  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["val1"],
      "action": "type_changes",
      "value": True,
      "type": "<class 'bool'>",
      "old_type": "<class 'str'>",
    }
  ]


def test_diff_multiple_dict_changes():
  @dataclass
  class C:
    val1: dict[str, str] = field(
      default_factory=lambda: {
        "k1": "v1",
        "k2": "v2",
        "k3": "v3",
      }
    )

  s1 = C()
  s2 = C(
    val1={
      "k1": "V1",
      "k2": "v2",
      "k4": "v4",
      "k5": "v5",
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", "k4"], "value": "v4", "action": "dictionary_item_added"},
    {"path": ["val1", "k5"], "value": "v5", "action": "dictionary_item_added"},
    {
      "path": ["val1", "k3"],
      "value": "v3",
      "action": "dictionary_item_removed",
    },
    {"path": ["val1", "k1"], "action": "values_changed", "value": "V1"},
  ]


def test_diff_nested_changes():
  @dataclass
  class B:
    val1: list[str | int]

  @dataclass
  class C:
    val1: dict[str, list[B]]

  s1 = C(
    val1={
      "k1": [B(val1=[1, 2, 3]), B(val1=[1])],
      "k2": [],
      "k3": [B(val1=[])],
    }
  )
  s2 = C(
    val1={
      "k1": [B(val1=[1, 2]), B(val1=[3, 4, 6, "2"])],
      "k2": [B(val1=[2, 2])],
      "k4": [B(val1=[])],
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["val1", "k4", 0],
      "value": {"val1": []},
      "action": "iterable_item_added",
    },
    {
      "path": ["val1", "k3"],
      "value": [{"val1": []}],
      "action": "dictionary_item_removed",
    },
    {
      "path": ["val1", "k1", 1, "val1", 0],
      "action": "values_changed",
      "value": 3,
    },
    {
      "path": ["val1", "k1", 1, "val1", 1],
      "value": 4,
      "action": "iterable_item_added",
    },
    {
      "path": ["val1", "k1", 1, "val1", 2],
      "value": 6,
      "action": "iterable_item_added",
    },
    {
      "path": ["val1", "k1", 1, "val1", 3],
      "value": "2",
      "action": "iterable_item_added",
    },
    {
      "path": ["val1", "k2", 0],
      "value": {"val1": [2, 2]},
      "action": "iterable_item_added",
    },
    {
      "path": ["val1", "k1", 0, "val1", 2],
      "value": 3,
      "action": "iterable_item_removed",
    },
  ]


def test_diff_weird_str_dict_keys():
  @dataclass
  class C:
    val1: dict[str, str] = field(
      default_factory=lambda: {
        "k-1": "v1",
        "k.2": "v2",
        "k 3": "v3",
      }
    )

  s1 = C()
  s2 = C(
    val1={
      "k-1": "V1",
      "k.2": "v2",
      "k 3": "v4",
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", "k-1"], "action": "values_changed", "value": "V1"},
    {"path": ["val1", "k 3"], "action": "values_changed", "value": "v4"},
  ]


def test_diff_int_dict_keys():
  @dataclass
  class C:
    val1: dict[int, str] = field(
      default_factory=lambda: {
        1: "v1",
      }
    )

  s1 = C()
  s2 = C(
    val1={
      1: "V1",
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", 1], "action": "values_changed", "value": "V1"}
  ]


# This looks like a bug.
def test_diff_tuple_dict_keys():
  @dataclass
  class C:
    val1: dict[tuple[int, int], str] = field(
      default_factory=lambda: {
        (1, 2): "v1",
      }
    )

  s1 = C()
  s2 = C(
    val1={
      (1, 2): "V1",
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", 1, 2], "action": "values_changed", "value": "V1"}
  ]


def test_diff_multiple_iterable_changes():
  @dataclass
  class C:
    val1: list[int] = field(default_factory=lambda: [1, 2, 3, 4, 5, 6, 7])

  s1 = C()
  s2 = C(val1=[2, 3, 3, 4, 6])

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", 2], "value": 3, "action": "iterable_item_added"},
    {"path": ["val1", 0], "value": 1, "action": "iterable_item_removed"},
    {"path": ["val1", 4], "value": 5, "action": "iterable_item_removed"},
    {"path": ["val1", 6], "value": 7, "action": "iterable_item_removed"},
  ]


def test_diff_multiple_iterable_deletions():
  @dataclass
  class C:
    val1: list[int] = field(default_factory=lambda: [1, 2, 3, 4, 5, 6, 7])
    val2: dict[str, list[int]] = field(
      default_factory=lambda: {
        "val2A": [10, 20, 30, 40, 50, 60, 70],
      }
    )

  s1 = C()
  s2 = C(
    val1=[2, 4, 6, 7],
    val2={
      "val2A": [10, 20, 40, 60, 70],
    },
  )

  assert json.loads(diff_state(s1, s2)) == [
    {"path": ["val1", 0], "value": 1, "action": "iterable_item_removed"},
    {"path": ["val1", 2], "value": 3, "action": "iterable_item_removed"},
    {"path": ["val1", 4], "value": 5, "action": "iterable_item_removed"},
    {
      "path": ["val2", "val2A", 2],
      "value": 30,
      "action": "iterable_item_removed",
    },
    {
      "path": ["val2", "val2A", 4],
      "value": 50,
      "action": "iterable_item_removed",
    },
  ]


def test_diff_pandas():
  @dataclass
  class C:
    data: pd.DataFrame

  s1 = C(data=pd.DataFrame(data={"Strings": ["Hello", "World"]}))
  s2 = C(data=pd.DataFrame(data={"Strings": ["Hello", "Universe"]}))

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["data"],
      "action": "data_frame_changed",
      "value": {
        "__pandas.DataFrame__": '{"schema":{"fields":[{"name":"index","type":"integer"},{"name":"Strings","type":"string"}],"primaryKey":["index"],"pandas_version":"1.4.0"},"data":[{"index":0,"Strings":"Hello"},{"index":1,"Strings":"Universe"}]}'
      },
    }
  ]


def test_diff_nested_pandas():
  @dataclass
  class C:
    data: dict[str, list[pd.DataFrame]]

  s1 = C(data={"test": [pd.DataFrame(data={"Strings": ["Hello", "World"]})]})
  s2 = C(
    data={
      "test": [
        pd.DataFrame(data={"Strings": ["Hello", "Universe"]}),
        pd.DataFrame(data={"Strings": ["Hola", "Universe"]}),
      ]
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["data", "test", 1],
      "value": {
        "__pandas.DataFrame__": '{"schema":{"fields":[{"name":"index","type":"integer"},{"name":"Strings","type":"string"}],"primaryKey":["index"],"pandas_version":"1.4.0"},"data":[{"index":0,"Strings":"Hola"},{"index":1,"Strings":"Universe"}]}'
      },
      "action": "iterable_item_added",
    },
    {
      "path": ["data", "test", 0],
      "action": "data_frame_changed",
      "value": {
        "__pandas.DataFrame__": '{"schema":{"fields":[{"name":"index","type":"integer"},{"name":"Strings","type":"string"}],"primaryKey":["index"],"pandas_version":"1.4.0"},"data":[{"index":0,"Strings":"Hello"},{"index":1,"Strings":"Universe"}]}'
      },
    },
  ]


def test_diff_uploaded_file():
  @dataclass
  class C:
    data: UploadedFile

  s1 = C(data=UploadedFile())
  s2 = C(
    data=UploadedFile(b"data", name="file.png", size=10, mime_type="image/png")
  )

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["data"],
      "action": "mesop_uploaded_file_changed",
      "value": {
        "__mesop.UploadedFile__": {
          "contents": "ZGF0YQ==",
          "name": "file.png",
          "size": 10,
          "mime_type": "image/png",
        },
      },
    }
  ]


def test_diff_uploaded_file_same_no_diff():
  @dataclass
  class C:
    data: UploadedFile

  s1 = C(
    data=UploadedFile(b"data", name="file.png", size=10, mime_type="image/png")
  )
  s2 = C(
    data=UploadedFile(b"data", name="file.png", size=10, mime_type="image/png")
  )

  assert json.loads(diff_state(s1, s2)) == []


def test_diff_set():
  @dataclass
  class C:
    val1: set[int] = field(default_factory=lambda: {1, 2, 3})

  s1 = C()
  s2 = C(val1={1, 5})

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["val1", "__python.set__"],
      "value": 2,
      "action": "set_item_removed",
    },
    {
      "path": ["val1", "__python.set__"],
      "value": 3,
      "action": "set_item_removed",
    },
    {
      "path": ["val1", "__python.set__"],
      "value": 5,
      "action": "set_item_added",
    },
  ]


def test_diff_bytes():
  @dataclass
  class C:
    val1: bytes = b"val1"

  s1 = C()
  s2 = C(val1=b"VAL1")

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["val1"],
      "action": "values_changed",
      "value": {
        "__python.bytes__": "VkFMMQ=="
      },  # Check if value is base64 encoded without asserting exact value
    }
  ]


def test_diff_not_dataclass():
  class C:
    val1: set[int] = field(default_factory=lambda: {1, 2, 3})

  with pytest.raises(MesopException):
    diff_state(C(), "s2")

  with pytest.raises(MesopException):
    diff_state("s1", C())


def test_diff_dates():
  @dataclass
  class C:
    val1: set = field(default_factory=set)

  s1 = C()
  s2 = C(
    val1={
      datetime(1972, 2, 2, tzinfo=timezone.utc),
      datetime(2005, 10, 12, tzinfo=timezone(timedelta(hours=-5))),
      datetime(2024, 12, 5, tzinfo=timezone(timedelta(hours=5, minutes=30))),
    }
  )

  assert json.loads(diff_state(s1, s2)) == [
    {
      "path": ["val1", "__python.set__"],
      "value": {"__datetime.datetime__": "2024-12-05T00:00:00+05:30"},
      "action": "set_item_added",
    },
    {
      "path": ["val1", "__python.set__"],
      "value": {"__datetime.datetime__": "1972-02-02T00:00:00+00:00"},
      "action": "set_item_added",
    },
    {
      "path": ["val1", "__python.set__"],
      "value": {"__datetime.datetime__": "2005-10-12T00:00:00-05:00"},
      "action": "set_item_added",
    },
  ]


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
