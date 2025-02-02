"""Basic Demo Gemini Live API integration with Mesop

Demonstrates the following:

- Setting up web socket connection to Gemini Live API via client
- Playing audio responses from Gemini Live API
- Sending audio input via user's microphone to Gemini Live API
- Sending video frames via user's webcam to Gemini Live API
- Can use custom tool to interact with Mesop UI
"""

import json
import os
import time
from dataclasses import field
from typing import Literal

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.gemini_live.audio_player import audio_player
from mesop.examples.web_component.gemini_live.audio_recorder import (
  audio_recorder,
)
from mesop.examples.web_component.gemini_live.gemini_live import gemini_live
from mesop.examples.web_component.gemini_live.video_recorder import (
  video_recorder,
)

VoiceName = Literal["Aoede", "Charon", "Fenrir", "Kore", "Puck"]
GeminiModel = Literal["gemini-2.0-flash-exp"]

_SYSTEM_INSTRUCTIONS = """
You are friendly chat bot that interacts with the user.

You have access to the following tool:

- get_box: Gets the contents of a box by name.

When the user asks you to open a box. Use the "get_box" tool. The box will return a
question. Ask the user the question inside the box.
""".strip()


def make_gemini_live_config(
  model: GeminiModel = "gemini-2.0-flash-exp",
  voice_name: VoiceName = "Puck",
):
  return json.dumps(
    {
      "model": f"models/{model}",
      "system_instruction": {
        "role": "user",
        "parts": [{"text": _SYSTEM_INSTRUCTIONS}],
      },
      "tools": [
        {
          "functionDeclarations": [
            {
              "name": "pick_box",
              "description": "Picks the box by name",
              "parameters": {
                "type": "OBJECT",
                "properties": {
                  "box_name": {
                    "type": "STRING",
                    "description": "Name of the box",
                  }
                },
                "required": ["box_name"],
              },
            }
          ]
        }
      ],
      "generation_config": {
        "temperature": 1,
        "response_modalities": ["audio"],
        "speech_config": {
          "voice_config": {"prebuilt_voice_config": {"voice_name": voice_name}}
        },
      },
    }
  )


@me.stateclass
class State:
  text_input: str = ""
  api_key: str = os.getenv("GOOGLE_API_KEY", "")
  gemini_live_enabled: bool = False
  gemini_live_config: str = make_gemini_live_config()
  audio_player_enabled: bool = False
  audio_recorder_state: Literal["disabled", "initializing", "recording"] = (
    "disabled"
  )
  video_recorder_enabled: bool = False
  video_recorder_state: Literal["disabled", "initializing", "recording"] = (
    "disabled"
  )
  input_prompt: str = ""
  tool_call_responses: str
  boxes: dict[str, str] = field(
    default_factory=lambda: {
      "green": "Who is the first president?",
      "blue": "What is the capital of Spain?",
      "red": "What is the tallest mountain?",
    }
  )
  opened_boxes: set[str] = field(default_factory=set)


@me.page(
  path="/web_component/gemini_live/demo",
  title="Gemini Live Demo",
  security_policy=me.SecurityPolicy(
    allowed_connect_srcs=["wss://generativelanguage.googleapis.com"],
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ],
  ),
)
def page():
  state = me.state(State)
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.input(
      label="Google API Key",
      on_input=on_input_api_key,
      readonly=state.gemini_live_enabled,
      style=me.Style(width="100%"),
      type="password",
      value=state.api_key,
    )

    me.input(
      label="Send message",
      on_enter=on_send_prompt,
      readonly=not state.gemini_live_enabled,
      style=me.Style(width="100%"),
      value=state.text_input,
    )

    with me.box(style=me.Style(display="flex", flex_direction="row", gap=10)):
      gemini_live_button()

      audio_player_button()

      audio_recorder_button()

      video_recorder_button()

    with me.box(style=me.Style(margin=me.Margin(top=15))):
      video_recorder(
        enabled=state.video_recorder_enabled,
        state=state.video_recorder_state,
        on_state_change=on_video_recorder_state_change,
      )

    me.text(
      "Pick a box",
      type="headline-5",
      style=me.Style(margin=me.Margin.symmetric(vertical=15)),
    )
    with me.box(style=me.Style(display="flex", gap=15)):
      for label, question in state.boxes.items():
        mystery_box(label, question)


@me.component
def mystery_box(label: str, question: str):
  state = me.state(State)
  with me.box(
    key=label,
    on_click=click_mystery_box,
    style=me.Style(
      background=label,
      cursor="pointer",
      padding=me.Padding.all(15),
    ),
  ):
    if label in state.opened_boxes:
      me.text(question, style=me.Style(color="#fff", text_align="center"))
    else:
      me.text(
        label,
        style=me.Style(color="#fff", text_align="center", font_weight="bold"),
      )


@me.component
def gemini_live_button():
  state = me.state(State)
  with gemini_live(
    api_config=state.gemini_live_config,
    api_key=state.api_key,
    enabled=state.gemini_live_enabled,
    input_prompt=state.input_prompt,
    on_start=on_gemini_live_started,
    on_stop=on_gemini_live_stopped,
    on_tool_call=on_tool_call,
    tool_call_responses=state.tool_call_responses,
  ):
    with me.tooltip(message=get_gemini_live_tooltip()):
      with me.content_button(
        disabled=not state.api_key,
        style=style_gemini_live_button(),
        type="icon",
      ):
        if state.gemini_live_enabled:
          me.icon(icon="stop")
        else:
          me.icon(icon="play_arrow")


@me.component
def audio_player_button():
  state = me.state(State)
  with audio_player(
    enabled=state.audio_player_enabled,
    on_play=on_audio_play,
    on_stop=on_audio_stop,
  ):
    with me.tooltip(message=get_audio_player_tooltip()):
      with me.content_button(
        disabled=True,
        style=style_audio_button(),
        type="icon",
      ):
        if state.audio_player_enabled:
          me.icon(icon="volume_up")
        else:
          me.icon(icon="volume_mute")


@me.component
def audio_recorder_button():
  state = me.state(State)
  with audio_recorder(
    state=state.audio_recorder_state,
    on_state_change=on_audio_recorder_state_change,
  ):
    with me.tooltip(message=get_audio_recorder_tooltip()):
      with me.content_button(
        disabled=not state.gemini_live_enabled,
        style=style_mic_button(),
        type="icon",
      ):
        if state.audio_recorder_state == "initializing":
          me.icon(icon="pending")
        else:
          me.icon(icon="mic")


@me.component
def video_recorder_button():
  state = me.state(State)
  with me.tooltip(message=get_video_recorder_tooltip()):
    with me.content_button(
      on_click=on_click_video_recorder_button,
      disabled=not state.gemini_live_enabled,
      style=style_video_button(),
      type="icon",
    ):
      if state.video_recorder_state == "initializing":
        me.icon(icon="pending")
      else:
        me.icon(icon="videocam")


def get_gemini_live_tooltip() -> str:
  state = me.state(State)
  if state.gemini_live_enabled:
    return "Disconnect"
  if state.api_key:
    return "Connect"
  return "Enter API Key first."


def get_audio_player_tooltip() -> str:
  state = me.state(State)
  if state.audio_player_enabled:
    return "Audio playing"
  if state.gemini_live_enabled:
    return "Audio not playing"
  return "Audio disabled"


def get_audio_recorder_tooltip() -> str:
  state = me.state(State)
  if state.audio_recorder_state == "initializing":
    "Microphone initializing"
  if state.audio_recorder_state == "recording":
    return "Microphone on"
  if state.gemini_live_enabled:
    return "Microphone muted"
  return "Microphone disabled"


def get_video_recorder_tooltip() -> str:
  state = me.state(State)
  if state.video_recorder_state == "initializing":
    "Webcam initializing"
  if state.video_recorder_state == "recording":
    return "Webcam on"
  if state.gemini_live_enabled:
    return "Webcam off"
  return "Webcam disabled"


def on_audio_play(e: mel.WebEvent):
  """Event for when audio player play button was clicked."""
  me.state(State).audio_player_enabled = True


def on_audio_stop(e: mel.WebEvent):
  """Event for when audio player stop button was clicked."""
  me.state(State).audio_player_enabled = False


def on_audio_recorder_state_change(e: mel.WebEvent):
  """Event for when audio recorder state changes."""
  me.state(State).audio_recorder_state = e.value


def on_click_video_recorder_button(e: me.ClickEvent):
  """Event for when the video recorder button is clicked."""
  state = me.state(State)
  state.video_recorder_enabled = not state.video_recorder_enabled


def on_video_recorder_state_change(e: mel.WebEvent):
  """Event for when audio recorder state changes."""
  me.state(State).video_recorder_state = e.value


def on_gemini_live_started(e: mel.WebEvent):
  """Event for when Gemin Live API start button was clicked."""
  me.state(State).gemini_live_enabled = True


def on_gemini_live_stopped(e: mel.WebEvent):
  """Event for when Gemin Live API stop button was clicked."""
  state = me.state(State)
  state.gemini_live_enabled = False


def on_send_prompt(e: me.InputEnterEvent):
  state = me.state(State)
  state.text_input = e.value
  state.input_prompt = e.value
  yield
  time.sleep(0.3)
  state.text_input = ""
  yield


def on_input_api_key(e: me.InputEvent):
  """Captures Google API key input"""
  state = me.state(State)
  state.api_key = e.value


def click_mystery_box(e: me.ClickEvent):
  me.state(State).input_prompt = "I want to pick the box with the name " + e.key


def on_tool_call(e: mel.WebEvent):
  """Handle custom tool request calls from Gemini Live API."""
  state = me.state(State)
  tool_calls = json.loads(e.value["toolCalls"])

  responses = []
  for tool_call in tool_calls:
    result = None
    if tool_call["name"] == "pick_box":
      result = pick_box(tool_call["args"]["box_name"])

    if result:
      responses.append(
        {
          "id": tool_call["id"],
          "name": tool_call["name"],
          "response": {
            "result": result,
          },
        }
      )

  if responses:
    state.tool_call_responses = json.dumps(responses)


def pick_box(box_name: str) -> str:
  """Custom tool function that gets the question with the given box name."""
  state = me.state(State)
  if box_name not in state.boxes:
    return "No box found"
  elif box_name in state.opened_boxes:
    return "You already opened that box"
  else:
    state.opened_boxes.add(box_name)
    return state.boxes[box_name]


def style_gemini_live_button() -> me.Style:
  state = me.state(State)
  if not state.api_key:
    return me.Style()
  if state.gemini_live_enabled:
    return me.Style(
      background=me.theme_var("error"), color=me.theme_var("on-error")
    )
  return me.Style(
    background=me.theme_var("primary"), color=me.theme_var("on-primary")
  )


def style_audio_button() -> me.Style:
  state = me.state(State)
  if state.audio_player_enabled:
    return me.Style(
      background=me.theme_var("tertiary"), color=me.theme_var("on-tertiary")
    )
  return me.Style()


def style_mic_button() -> me.Style:
  state = me.state(State)
  if state.audio_recorder_state == "recording":
    return me.Style(
      background=me.theme_var("tertiary"), color=me.theme_var("on-tertiary")
    )
  if state.gemini_live_enabled:
    return me.Style(
      background=me.theme_var("error"), color=me.theme_var("on-error")
    )
  return me.Style()


def style_video_button() -> me.Style:
  state = me.state(State)
  if state.video_recorder_state == "recording":
    return me.Style(
      background=me.theme_var("tertiary"), color=me.theme_var("on-tertiary")
    )
  if state.gemini_live_enabled:
    return me.Style(
      background=me.theme_var("error"), color=me.theme_var("on-error")
    )
  return me.Style()
