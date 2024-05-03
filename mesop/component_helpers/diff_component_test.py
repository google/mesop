import pytest

import mesop.protos.ui_pb2 as pb
from mesop.component_helpers.helper import diff_component


def create_default_single_component():
  return pb.Component(
    key=pb.Key(key="key"),
    style=pb.Style(color="red", columns="1"),
    style_debug_json="debug json string",
    type=pb.Type(
      name=pb.ComponentName(core_module=True, fn_name="test"), value=b"value"
    ),
    source_code_location=pb.SourceCodeLocation(module="x", line=1, col=2),
  )


def test_single_component_no_diff():
  c1 = create_default_single_component()

  assert diff_component(c1, c1) == pb.ComponentDiff()


def test_single_component_key_diff():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.key.CopyFrom(pb.Key(key="key2"))

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    key=pb.Key(key="key2"),
  )


def test_single_component_source_code_location_diff():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.source_code_location.CopyFrom(
    pb.SourceCodeLocation(module="y", line=10, col=20)
  )

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    update_strategy_source_code_location=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    source_code_location=pb.SourceCodeLocation(module="y", line=10, col=20),
  )


def test_single_component_style_diff():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.style.CopyFrom(pb.Style(width="100px"))

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    update_strategy_style=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    style=pb.Style(width="100px"),
  )


def test_single_component_style_debug_json_diff():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.style_debug_json = "updated json"

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    update_strategy_style_debug_json=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    style_debug_json="updated json",
  )


def test_single_component_type_diff():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.type.CopyFrom(
    pb.Type(
      name=pb.ComponentName(core_module=True, fn_name="test-diff"),
      value=b"value2",
    )
  )

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    update_strategy_type=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    type=pb.Type(
      name=pb.ComponentName(core_module=True, fn_name="test-diff"),
      value=b"value2",
    ),
  )


def test_single_component_multiple_diffs():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.key.CopyFrom(pb.Key(key="key2"))
  c2.style.CopyFrom(pb.Style(width="100px"))

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    key=pb.Key(key="key2"),
    update_strategy_style=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    style=pb.Style(width="100px"),
  )


def test_add_child_component():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2.children.append(c2_c1)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
        component=create_default_single_component(),
      )
    ],
  )


def test_add_multiple_child_components():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c2 = create_default_single_component()
  c2.children.append(c2_c1)
  c2.children.append(c2_c2)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
        component=c2_c1,
      ),
      pb.ComponentDiff(
        index=1,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
        component=c2_c2,
      ),
    ],
  )


def test_add_child_component_sub_tree():
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c1_c1 = create_default_single_component()
  c2_c1.children.append(c2_c1_c1)
  c2.children.append(c2_c1)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
        component=c2_c1,
      ),
    ],
  )


def test_add_child_child_component():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1.children.append(c1_c1)
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c1_c1 = create_default_single_component()
  c2_c1.children.append(c2_c1_c1)
  c2.children.append(c2_c1)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        children=[
          pb.ComponentDiff(
            index=0,
            diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
            component=c2_c1_c1,
          ),
        ],
      )
    ],
  )


def test_delete_child_component():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1.children.append(c1_c1)
  c2 = create_default_single_component()

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_DELETE,
      )
    ],
  )


def test_delete_multiple_child_components():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c2 = create_default_single_component()
  c1.children.append(c1_c1)
  c1.children.append(c1_c2)
  c2 = create_default_single_component()

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_DELETE,
      ),
      pb.ComponentDiff(
        index=1,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_DELETE,
      ),
    ],
  )


def test_delete_child_component_sub_tree():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c1_c1 = create_default_single_component()
  c1_c1.children.append(c1_c1_c1)
  c1.children.append(c1_c1)

  c2 = create_default_single_component()

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_DELETE,
      ),
    ],
  )


def test_delete_child_child_component():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c1_c1 = create_default_single_component()
  c1_c1.children.append(c1_c1_c1)
  c1.children.append(c1_c1)
  c2 = create_default_single_component()

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_DELETE,
      ),
    ],
  )


def test_update_child_component():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1.children.append(c1_c1)
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c1.key.CopyFrom(pb.Key(key="key2"))
  c2.children.append(c2_c1)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
        key=pb.Key(key="key2"),
      )
    ],
  )


def test_update_multiple_child_components():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c2 = create_default_single_component()
  c1.children.append(c1_c1)
  c1.children.append(c1_c2)
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c1.key.CopyFrom(pb.Key(key="key2"))
  c2_c2 = create_default_single_component()
  c2_c2.key.CopyFrom(pb.Key(key="key3"))
  c2.children.append(c2_c1)
  c2.children.append(c2_c2)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
        key=pb.Key(key="key2"),
      ),
      pb.ComponentDiff(
        index=1,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
        key=pb.Key(key="key3"),
      ),
    ],
  )


def test_update_child_child_component():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c1_c1 = create_default_single_component()
  c1_c1.children.append(c1_c1_c1)
  c1.children.append(c1_c1)
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c1_c1 = create_default_single_component()
  c2_c1_c1.key.CopyFrom(pb.Key(key="key3"))
  c2_c1.children.append(c2_c1_c1)
  c2.children.append(c2_c1)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        children=[
          pb.ComponentDiff(
            index=0,
            diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
            update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
            key=pb.Key(key="key3"),
          )
        ],
      ),
    ],
  )


def test_swapped_child_components_will_update_fields():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c1.key.CopyFrom(pb.Key(key="key2"))
  c1_c2 = create_default_single_component()
  c1.children.append(c1_c1)
  c1.children.append(c1_c2)
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c2 = create_default_single_component()
  c2_c2.key.CopyFrom(pb.Key(key="key2"))
  c2.children.append(c2_c1)
  c2.children.append(c2_c2)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
        key=pb.Key(key="key"),
      ),
      pb.ComponentDiff(
        index=1,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
        key=pb.Key(key="key2"),
      ),
    ],
  )


def test_displaced_child_component_will_update_and_add_component():
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c1.key.CopyFrom(pb.Key(key="key2"))
  c1.children.append(c1_c1)
  c2 = create_default_single_component()
  c2_c1 = create_default_single_component()
  c2_c2 = create_default_single_component()
  c2_c2.key.CopyFrom(pb.Key(key="key2"))
  c2.children.append(c2_c1)
  c2.children.append(c2_c2)

  assert diff_component(c1, c2) == pb.ComponentDiff(
    diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
    children=[
      pb.ComponentDiff(
        index=0,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_UPDATE,
        update_strategy_key=pb.ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
        key=pb.Key(key="key"),
      ),
      pb.ComponentDiff(
        index=1,
        diff_type=pb.ComponentDiff.DiffType.DIFF_TYPE_ADD,
        component=c2_c2,
      ),
    ],
  )


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
