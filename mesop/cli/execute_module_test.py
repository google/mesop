from mesop.cli.execute_module import get_app_modules, get_module_name


def test_get_module_name():
  assert (
    # Intentionally use a fake workspace name so this test
    # behaves the same way both upstream and downstream.
    get_module_name("workspace_name/mesop/example_index.py")
    == "mesop.example_index"
  )


def test_get_app_modules():
  assert get_app_modules(
    "mesop.example_index",
    loaded_module_names=set(
      [
        "mesop",
        "mesop.runtime",
        "mesop.example_index",
        "mesop.examples",
        "mesop.examples.index",
        "mesop.components.radio.radio",
        "mesop.components.radio.e2e.radio_app",
      ]
    ),
  ) == set(
    [
      "mesop.example_index",
      "mesop.examples",
      "mesop.examples.index",
      "mesop.components.radio.e2e.radio_app",
    ]
  )


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
