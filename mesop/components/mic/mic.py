from dataclasses import dataclass
from typing import Any, Callable

import mesop.components.mic.mic_pb2 as mic_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class AudioChunkEvent(MesopEvent):
  """Event representing a click on the table component cell.

  Attributes:
      row_index: DataFrame row index of the clicked cell in the table.
      col_index: DataFrame col index of the clicked cell in the table.
      key (str): key of the component that emitted this event.
  """

  data: bytes
  transcript: str


def map_event(event, key):
  chunk_event = mic_pb.AudioChunk()
  chunk_event.ParseFromString(event.bytes_value)
  return AudioChunkEvent(
    key=key.key,
    data=chunk_event.data,
    transcript=chunk_event.transcript,
  )


register_event_mapper(AudioChunkEvent, map_event)


@register_native_component
def mic(
  *,
  on_chunk=Callable[..., Any],
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
      on_chunk_event_handler_id=register_event_handler(
        on_chunk, AudioChunkEvent
      )
    ),
  )
