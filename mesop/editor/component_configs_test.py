import pytest

import mesop.protos.ui_pb2 as pb
from mesop.components.button.button import button
from mesop.editor.component_configs import (
  generate_component_config,
  get_component_configs,
)


def test_generate_component_config_button():
  proto = generate_component_config(button)
  assert proto.component_name == "button"
  assert proto.fields[0] == pb.EditorField(name="on_click")
  assert proto.fields[1] == pb.EditorField(
    name="type",
    type=pb.FieldType(
      string_literal_type=pb.StringLiteralType(
        literals=["raised", "flat", "stroked", "icon"]
      )
    ),
  )


def test_get_component_configs():
  assert len(get_component_configs()) == 15


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
