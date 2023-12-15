from dataclasses import dataclass
from typing import Any, Callable, Literal

from pydantic import validate_arguments

import mesop.components.component_name.component_name_pb2 as component_name_pb
from mesop.component_helpers import (
  handler_type,
  insert_component,
  register_event_mapper,
)
from mesop.events import MesopEvent

# INSERT_EVENTS


@validate_arguments
def component_name(
  *,
  # INSERT_COMPONENT_PARAMS
):
  """
  TODO_doc_string
  """
  insert_component(
    key=key,
    type_name="component_name",
    proto=component_name_pb.ComponentNameType(
      # INSERT_PROTO_CALLSITE
    ),
  )
