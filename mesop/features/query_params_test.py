# pyright: reportPrivateUsage=false

import pytest

from mesop.features.query_params import QueryParams
from mesop.runtime.context import Context


def test_query_params_iter():
  context = Context(get_handler=lambda x: None, states={})
  context._query_params = {
    "key1": ["k1value1", "k1value2"],
    "key2": ["value2"],
  }
  query_params = QueryParams(lambda: context)

  assert list(query_params) == ["key1", "key2"]
  assert {**query_params} == {
    "key1": "k1value1",
    "key2": "value2",
  }


def test_query_params_len():
  context = Context(get_handler=lambda x: None, states={})
  context._query_params = {
    "key1": ["value1"],
    "key2": ["value2"],
  }
  query_params = QueryParams(lambda: context)

  assert len(query_params) == 2


def test_query_params_str():
  context = Context(get_handler=lambda x: None, states={})
  context._query_params = {
    "key1": ["value1"],
    "key2": ["value2"],
  }
  query_params = QueryParams(lambda: context)

  assert str(query_params) == str({"key1": ["value1"], "key2": ["value2"]})


def test_query_params_getitem():
  context = Context(get_handler=lambda x: None, states={})
  context._query_params = {
    "key1": ["value1"],
    "key2": ["value2", "value3"],
  }
  query_params = QueryParams(lambda: context)

  assert query_params["key1"] == "value1"
  assert query_params["key2"] == "value2"

  assert "non-existent" not in query_params
  with pytest.raises(KeyError):
    query_params["non-existent"]


def test_query_params_get_all():
  context = Context(get_handler=lambda x: None, states={})
  context._query_params = {
    "key1": ["value1"],
    "key2": ["value2", "value3"],
  }
  query_params = QueryParams(lambda: context)

  assert query_params.get_all("key1") == ("value1",)
  assert query_params.get_all("key2") == ("value2", "value3")
  assert query_params.get_all("non-existent") == tuple()


def test_query_params_delitem():
  context = Context(get_handler=lambda x: None, states={})
  context._query_params = {"key1": ["value"]}
  query_params = QueryParams(lambda: context)

  del query_params["key1"]
  assert context._query_params.get("key1") is None


def test_query_params_setitem():
  context = Context(get_handler=lambda x: None, states={})
  query_params = QueryParams(lambda: context)

  query_params["key1"] = "value1"
  assert context._query_params["key1"] == ["value1"]

  query_params["key2"] = ["value2", "value3"]
  assert context._query_params["key2"] == ["value2", "value3"]


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
