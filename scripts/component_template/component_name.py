import mesop.components.component_name.component_name_pb2 as component_name_pb
from mesop.component_helpers import insert_component, register_native_component


@register_native_component
def component_name(
  *,
  label: str,
  key: str | None = None,
):
  """
  This function creates a component_name.

  Args:
      label: The text to be displayed
  """
  insert_component(
    key=key,
    type_name="component_name",
    proto=component_name_pb.ComponentNameType(
      label=label,
    ),
  )
