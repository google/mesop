import mesop.components.accordion.accordion_pb2 as accordion_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_native_component,
)


@register_native_component
def accordion(
  *,
  key: str | None = None,
):
  """
  This function creates an accordion.

  This is more of a visual component. It is used to style a group of expansion panel
  components in a unified and consistent way (as if they were one component -- i.e. an
  accordion).

  The mechanics of an accordion that only allows one expansion panel to be open at a
  time, must be implemented manually, but is easy to do with Mesop state and event
  handlers.
  """
  return insert_composite_component(
    key=key,
    type_name="accordion",
    proto=accordion_pb.AccordionType(),
  )
