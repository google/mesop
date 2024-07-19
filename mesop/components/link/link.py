import mesop.components.link.link_pb2 as link_pb
from mesop.component_helpers import insert_component, register_native_component


@register_native_component
def link(
  *,
  label: str,
  key: str | None = None,
):
  """
  This function creates a link.

  Args:
      label: The text to be displayed
  """
  insert_component(
    key=key,
    type_name="link",
    proto=link_pb.LinkType(
      label=label,
    ),
  )
