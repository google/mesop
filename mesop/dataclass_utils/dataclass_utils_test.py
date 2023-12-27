from dataclasses import dataclass, field

from mesop.dataclass_utils.dataclass_utils import (
  dataclass_with_defaults,
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
  strs: list[str] = field(default_factory=list)


JSON_STR = """{"b": {"c": {"val": "<init>"}},
"list_b": [
  {"c": {"val": "1"}},
  {"c": {"val": "2"}}
], "strs": ["a", "b"]}"""


@dataclass_with_defaults
class DataclassNoDefaults:
  foo: int


@dataclass_with_defaults
class NestedDataclassNoDefaults:
  a: DataclassNoDefaults
  list_a: list[DataclassNoDefaults]


def test_dataclass_defaults():
  d = DataclassNoDefaults()
  assert d.foo == 0


def test_dataclass_defaults_recursive():
  d = NestedDataclassNoDefaults()
  assert d.a.foo == 0
  assert d.list_a == []


def test_serialize_dataclass():
  val = serialize_dataclass(A())
  assert val == """{"b": {"c": {"val": "<init>"}}, "list_b": [], "strs": []}"""


def test_update_dataclass_from_json_nested_dataclass():
  b = B()
  update_dataclass_from_json(b, """{"c": {"val": "<init>"}}""")
  assert b.c.val == "<init>"

  a = A()
  update_dataclass_from_json(a, JSON_STR)
  assert a.b.c.val == "<init>"


def test_update_dataclass_from_json_list_nested_dataclass():
  a = A()
  update_dataclass_from_json(a, JSON_STR)
  assert a.list_b == [
    B(c=C(val="1")),
    B(c=C(val="2")),
  ]
  assert a.strs == ["a", "b"]


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
