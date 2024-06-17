import mesop.components.audio.audio_pb2 as audio_pb
from mesop.component_helpers import insert_component, register_native_component


@register_native_component
def audio(
  *, src: str | None = None, key: str | None = None, autoplay: bool = False
):
  """
  Creates an audio component.

  Args:
      src: The URL of the audio to be played.
      autoplay: boolean value indicating if the audio should be autoplayed or not. **Note**: There are autoplay restrictions in modern browsers, including Chrome, are designed to prevent audio or video from playing automatically without user interaction. This is intended to improve user experience and reduce unwanted interruptions
      key: The component [key](../components/index.md#component-key).
  """
  insert_component(
    key=key,
    type_name="audio",
    proto=audio_pb.AudioType(src=src, autoplay=autoplay),
  )
