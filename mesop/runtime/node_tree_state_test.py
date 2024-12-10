import pytest

import mesop.protos.ui_pb2 as pb
from mesop.runtime.context import NodeTreeState


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


def test_set_current_node():
  node_tree_state = NodeTreeState()
  current_component = create_default_single_component()
  node_tree_state.set_current_node(current_component)

  assert node_tree_state.current_node() == current_component


def test_set_previous_node_from_current_node():
  node_tree_state = NodeTreeState()
  current_component = create_default_single_component()
  node_tree_state.set_current_node(current_component)
  assert node_tree_state.previous_node() is None

  node_tree_state.set_previous_node_from_current_node()

  assert node_tree_state.previous_node() == current_component


def test_reset_current_node():
  node_tree_state = NodeTreeState()
  current_component = create_default_single_component()
  node_tree_state.set_current_node(current_component)
  assert node_tree_state.current_node() == current_component

  node_tree_state.reset_current_node()

  assert node_tree_state.current_node() == pb.Component()


def test_reset_previous_node():
  node_tree_state = NodeTreeState()
  node_tree_state.set_previous_node_from_current_node()
  assert node_tree_state.previous_node() == node_tree_state.current_node()

  node_tree_state.reset_previous_node()

  assert node_tree_state.previous_node() is None


def test_save_current_node_as_slot():
  node_tree_state = NodeTreeState()
  c1 = create_default_single_component()
  c1_c1 = create_default_single_component()
  c1_c2 = create_default_single_component()
  c1.children.append(c1_c1)
  c1.children.append(c1_c2)
  node_tree_state.set_current_node(c1)

  node_tree_state.save_current_node_as_slot()

  node_slots = node_tree_state.node_slots()
  assert len(node_slots) == 1
  assert node_slots[0].name == ""
  assert node_slots[0].parent_node == c1
  assert node_slots[0].insertion_index == 2


def test_save_current_node_as_slot_with_name():
  node_tree_state = NodeTreeState()
  current_node = create_default_single_component()
  node_tree_state.set_current_node(current_node)

  node_tree_state.save_current_node_as_slot("test")

  node_slots = node_tree_state.node_slots()
  assert len(node_slots) == 1
  assert node_slots[0].name == "test"
  assert node_slots[0].parent_node == current_node
  assert node_slots[0].insertion_index == 0


def test_multiple_save_current_node_as_slot():
  node_tree_state = NodeTreeState()
  c1 = create_default_single_component()
  c2 = create_default_single_component()
  c2.style.CopyFrom(pb.Style(color="blue"))
  node_tree_state.set_current_node(c1)
  node_tree_state.save_current_node_as_slot()
  node_tree_state.set_current_node(c2)
  node_tree_state.save_current_node_as_slot()

  node_slots = node_tree_state.node_slots()
  assert len(node_slots) == 2
  assert node_slots[0].parent_node == c1
  assert node_slots[1].parent_node == c2


def test_clear_node_slots_to_first_null_slot():
  node_tree_state = NodeTreeState()
  c1 = create_default_single_component()
  node_tree_state.set_current_node(c1)
  node_tree_state.save_current_node_as_slot()
  node_tree_state.add_null_slot()
  c2 = create_default_single_component()
  c2.style.CopyFrom(pb.Style(color="blue"))
  node_tree_state.set_current_node(c2)
  node_tree_state.save_current_node_as_slot()
  c3 = create_default_single_component()
  node_tree_state.set_current_node(c3)
  c2.style.CopyFrom(pb.Style(color="green"))
  node_tree_state.save_current_node_as_slot()

  node_tree_state.clear_node_slots_to_first_null_slot()
  assert len(node_tree_state.node_slots()) == 1
  assert node_tree_state.node_slots()[0].parent_node == c1

  node_tree_state.clear_node_slots_to_first_null_slot()
  assert len(node_tree_state.node_slots()) == 0


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
