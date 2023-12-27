from mesop.cli.execute_module import get_app_modules, get_module_name


def test_get_module_name():
  assert (
    get_module_name("mesop/mesop/example_index.py") == "mesop.example_index"
  )


def test_get_app_modules():
  assert get_app_modules(
    "mesop.testing.index",
    loaded_module_names=set(
      [
        "mesop",
        "mesop.testing",
        "mesop.testing.sibling_module",
        "mesop.testing.sub_module.sub_module2",
        "mesop.testingwithpostfix",
        "mesop.separate_package",
      ]
    ),
  ) == set(
    [
      "mesop.testing",
      "mesop.testing.sibling_module",
      "mesop.testing.sub_module.sub_module2",
    ]
  )


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
