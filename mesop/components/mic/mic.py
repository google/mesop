import mesop.components.mic.mic_pb2 as mic_pb
from mesop.component_helpers import insert_component, register_native_component


@register_native_component
def mic(
  *,
  label: str,
  key: str | None = None,
):
  """
  This function creates a mic.

  Args:
      label: The text to be displayed
  """
  insert_component(
    key=key,
    type_name="mic",
    proto=mic_pb.MicType(
      label=label,
    ),
  )
