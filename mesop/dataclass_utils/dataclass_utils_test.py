from dataclasses import dataclass, field
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

import mesop.protos.ui_pb2 as pb
from mesop.components.uploader.uploaded_file import UploadedFile
from mesop.dataclass_utils.dataclass_utils import (
  dataclass_with_defaults,
  has_parent,
  serialize_dataclass,
  update_dataclass_from_json,
)


@dataclass
class C:
  val: str = "<init>"


@dataclass
class B:
  c: C = field(default_factory=C)


@dataclass
class A:
  b: B = field(default_factory=B)
  list_b: list[B] = field(default_factory=list)
  dates: list[datetime] = field(default_factory=lambda: [datetime(1974, 1, 1)])
  strs: list[str] = field(default_factory=list)
  str_dict: dict[str, str] = field(default_factory=dict)


@dataclass
class WithPandasDataFrame:
  val: pd.DataFrame | None = None


@dataclass
class WithBytes:
  data: bytes = b""


@dataclass
class WithUploadedFile:
  data: UploadedFile = field(default_factory=UploadedFile)


JSON_STR = """{"b": {"c": {"val": "<init>"}},
"list_b": [
  {"c": {"val": "1"}},
  {"c": {"val": "2"}}
],
"dates": [
  {"__datetime.datetime__": "1972-01-01T02:00:30"},
  {"__datetime.datetime__": "2024-06-12T05:01:30"}
],
"strs": ["a", "b"]}"""


@dataclass_with_defaults
class DataclassNoDefaults:
  foo: int
  dict: dict[str, str]


class UnannotatedClass:
  val: str


@dataclass_with_defaults
class NestedDataclassNoDefaults:
  a: DataclassNoDefaults
  list_a: list[DataclassNoDefaults]
  unannotated: UnannotatedClass


def test_dataclass_defaults():
  d = DataclassNoDefaults()
  assert d.foo == 0


def test_dataclass_defaults_recursive():
  d = NestedDataclassNoDefaults()
  assert d.a.foo == 0
  assert d.list_a == []
  assert d.unannotated.val == ""


def test_dataclass_field_defaults_works_with_already_annotated_nested_class():
  @dataclass
  class NestedDataclass:
    val: str = field(default="<default>")

  @dataclass_with_defaults
  class RootDataclass:
    nested: NestedDataclass

  instance = RootDataclass()
  assert instance.nested.val == "<default>"


def test_dataclass_defaults_works_with_already_annotated_nested_class():
  @dataclass
  class NestedDataclass:
    val: str = "default"

  @dataclass_with_defaults
  class RootDataclass:
    nested: NestedDataclass

  instance = RootDataclass()
  assert instance.nested.val == "default"


def test_dataclass_defaults_works_with_already_annotated_nested_class_fails_without_default():
  @dataclass
  class NestedDataclass:
    val: str

  @dataclass_with_defaults
  class RootDataclass:
    nested: NestedDataclass

  with pytest.raises(TypeError) as exc_info:
    RootDataclass()
  assert "missing 1 required positional argument: 'val'" in str(exc_info.value)


def test_serialize_dataclass():
  val = serialize_dataclass(A())
  assert (
    val
    == """{"b": {"c": {"val": "<init>"}}, "list_b": [], "dates": [{"__datetime.datetime__": "1974-01-01T00:00:00"}], "strs": [], "str_dict": {}}"""
  )


def test_serialize_pandas_dataframe():
  df = pd.DataFrame(
    data={
      "NA": [pd.NA, pd.NA],
      "Bools": [True, np.bool_(False)],
      "Ints": [101, np.int64(-55)],
      "Floats": [2.3, np.float64(-3.000000003)],
      "Strings": ["Hello", "World"],
      "DateTimes": [
        pd.Timestamp("20180310"),
        pd.Timestamp("20230310"),
      ],
    }
  )

  serialized_dataclass = serialize_dataclass(WithPandasDataFrame(val=df))

  json_data = df.to_json(orient="table")
  assert json_data is not None
  assert (
    serialized_dataclass
    == '{"val": {"__pandas.DataFrame__": "'
    + json_data.replace('"', '\\"')
    + '"}}'
  )


def test_serialize_uploaded_file():
  serialized_dataclass = serialize_dataclass(
    WithUploadedFile(
      data=UploadedFile(
        b"data", name="file.png", size=10, mime_type="image/png"
      )
    )
  )

  assert (
    serialized_dataclass
    == '{"data": {"__mesop.UploadedFile__": {"contents": "ZGF0YQ==", "name": "file.png", "size": 10, "mime_type": "image/png"}}}'
  )


@pytest.mark.parametrize(
  "input_bytes, expected_json",
  [
    (b"hello world", '{"data": {"__python.bytes__": "aGVsbG8gd29ybGQ="}}'),
    (b"", '{"data": {"__python.bytes__": ""}}'),
  ],
)
def test_serialize_bytes(input_bytes, expected_json):
  serialized_dataclass = serialize_dataclass(WithBytes(data=input_bytes))
  assert serialized_dataclass == expected_json


def test_update_dataclass_from_json_nested_dataclass():
  b = B()
  update_dataclass_from_json(b, """{"c": {"val": "<init>"}}""")
  assert b.c.val == "<init>"

  a = A()
  update_dataclass_from_json(a, JSON_STR)
  assert a.dates == [
    datetime(1972, 1, 1, 2, 0, 30),
    datetime(2024, 6, 12, 5, 1, 30),
  ]
  assert a.b.c.val == "<init>"


def test_update_dataclass_from_json_list_nested_dataclass():
  a = A()
  update_dataclass_from_json(a, JSON_STR)
  assert a.list_b == [
    B(c=C(val="1")),
    B(c=C(val="2")),
  ]
  assert a.strs == ["a", "b"]


def test_update_dataclass_with_pandas_dataframe():
  serialized_dataclass = serialize_dataclass(
    WithPandasDataFrame(
      val=pd.DataFrame(
        data={
          "NA": [pd.NA, pd.NA],
          "Bools": [True, np.bool_(False)],
          "Ints": [101, np.int64(-55)],
          "Floats": [2.3, np.float64(-3.000000003)],
          "Strings": ["Hello", "World"],
          "DateTimes": [
            pd.Timestamp("20180310"),
            pd.Timestamp("20230310"),
          ],
        }
      )
    )
  )
  pandas_dataframe_state = WithPandasDataFrame()

  update_dataclass_from_json(pandas_dataframe_state, serialized_dataclass)

  assert pandas_dataframe_state.val is not None
  assert pandas_dataframe_state.val.equals(
    pd.DataFrame(
      data={
        "NA": [
          np.nan,
          np.nan,
        ],  # Note that these became np.nan instead of pd.NA.
        "Bools": [True, np.bool_(False)],
        "Ints": [101, np.int64(-55)],
        "Floats": [2.3, np.float64(-3.000000003)],
        "Strings": ["Hello", "World"],
        "DateTimes": [
          pd.Timestamp("20180310"),
          pd.Timestamp("20230310"),
        ],
      }
    )
  )


def test_update_dataclass_with_uploaded_file():
  uploaded_file = UploadedFile(
    b"data", name="file.png", size=10, mime_type="image/png"
  )
  serialized_dataclass = serialize_dataclass(
    WithUploadedFile(data=uploaded_file)
  )
  uploaded_file_state = WithUploadedFile()
  update_dataclass_from_json(uploaded_file_state, serialized_dataclass)
  assert uploaded_file_state.data == uploaded_file


def test_update_dataclass_with_bytes():
  bytes_data = b"hello world"
  serialized_dataclass = serialize_dataclass(WithBytes(data=bytes_data))
  bytes_state = WithBytes()
  update_dataclass_from_json(bytes_state, serialized_dataclass)
  assert bytes_state.data == bytes_data


@dataclass_with_defaults
class StateWithDict:
  a_dict: dict[str, bool]


def test_serialize_deserialize_state_with_dict():
  state = StateWithDict()
  state.a_dict["a"] = True
  state.a_dict["b"] = False
  new_state = StateWithDict()
  update_dataclass_from_json(new_state, serialize_dataclass(state))
  assert new_state == state


@dataclass_with_defaults
class StateWithNestedDict:
  nested_dict: dict[str, dict[str, bool]]


def test_serialize_deserialize_state_with_nested_dict():
  state = StateWithNestedDict()
  state.nested_dict["a"] = {"inner": True, "inner2": False}
  state.nested_dict["b"] = {"val": True}
  new_state = StateWithNestedDict()
  update_dataclass_from_json(new_state, serialize_dataclass(state))
  assert new_state == state


@dataclass_with_defaults
class StateWithNestedList:
  nested_list: list[list[str]]


def test_serialize_deserialize_state_with_nested_list():
  state = StateWithNestedList()
  state.nested_list.append(["a", "b"])
  state.nested_list.append([])
  new_state = StateWithNestedList()
  update_dataclass_from_json(new_state, serialize_dataclass(state))
  assert new_state == state


@dataclass_with_defaults
class StateWithListDict:
  list_dict: list[dict[str, bool]]


def test_serialize_deserialize_state_with_list_dict():
  state = StateWithListDict()
  state.list_dict.append({"firstEl": True})
  state.list_dict.append({"2A": True, "2B": False})
  new_state = StateWithListDict()
  update_dataclass_from_json(new_state, serialize_dataclass(state))
  assert new_state == state


def test_serialize_deserialize_state_with_proto_throws():
  @dataclass_with_defaults
  class State:
    proto: pb.ComponentName

  state = State()

  with pytest.raises(Exception) as exc_info:
    serialize_dataclass(state)

  assert "Object of type ComponentName is not JSON serializable" in str(
    exc_info.value
  )


def test_dataclass_default_value_throws():
  with pytest.raises(Exception) as exc_info:

    @dataclass
    class MutableDataclass:
      str_value: str

    @dataclass_with_defaults
    class StateWithMutableDefaultDataclassValue:
      value: MutableDataclass = MutableDataclass(str_value="abc")

  assert (
    "Detected mutable default value for non-hashable type=MutableDataclass for attribute=value in class=StateWithMutableDefaultDataclassValue"
    in str(exc_info.value)
  )


def test_proto_without_default_does_not_throw():
  @dataclass_with_defaults
  class StateWithMutableProto:
    proto: pb.Style


def test_proto_with_default_throws():
  with pytest.raises(Exception) as exc_info:

    @dataclass_with_defaults
    class StateWithMutableProto:
      proto: pb.Style = pb.Style()

  assert "Detected mutable default value" in str(exc_info.value)


def test_proto_in_dataclass_without_default_does_not_throw():
  @dataclass
  class DataclassWithProto:
    style: pb.Style

  @dataclass_with_defaults
  class StateWithMutableProto:
    dataclass: DataclassWithProto


def test_proto_in_dataclass_with_default_throws():
  with pytest.raises(Exception) as exc_info:

    @dataclass
    class DataclassWithProto:
      style: pb.Style = pb.Style()  # noqa: RUF009 (intentionally do an anti-pattern to make sure exception is raised)

    @dataclass_with_defaults
    class StateWithMutableProto:
      dataclass: DataclassWithProto

  assert (
    "Detected mutable default value for non-hashable type=Style for attribute=style in class=DataclassWithProto"
    in str(exc_info.value)
  )


def test_proto_in_unannotated_class_without_default_does_not_throw():
  class UnannotatedClassWithProto:
    style: pb.Style

  @dataclass_with_defaults
  class StateWithMutableProto:
    dataclass: UnannotatedClassWithProto


def test_proto_in_unannotated_class_with_default_throws():
  with pytest.raises(Exception) as exc_info:

    class UnannotatedClassWithProto:
      style: pb.Style = pb.Style()

    @dataclass_with_defaults
    class StateWithMutableProto:
      dataclass: UnannotatedClassWithProto

  assert (
    "Detected mutable default value for non-hashable type=Style for attribute=style in class=UnannotatedClassWithProto"
    in str(exc_info.value)
  )


def test_has_parent_simple_class():
  class SimpleClass:
    val: str

  assert has_parent(SimpleClass) is False


def test_has_parent_dataclass():
  @dataclass
  class ADataclass:
    val: str

  assert has_parent(ADataclass) is False


def test_has_parent_child_class():
  class ParentClass:
    pass

  class ChildClass(ParentClass):
    val: str

  assert has_parent(ChildClass) is True
  assert has_parent(ParentClass) is False


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
