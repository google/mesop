import random
import time
from dataclasses import dataclass
from typing import Literal

import mesop as me

Role = Literal["user", "bot"]


@dataclass(kw_only=True)
class ChatMessage:
  """Chat message metadata."""

  role: Role = "user"
  content: str = ""
  edited: bool = False


@me.stateclass
class State:
  input: str
  output: list[ChatMessage]
  in_progress: bool


@me.page(path="/ai")
def page():
  state = me.state(State)
  with me.box(
    style=me.Style(
      color=me.theme_var("on-surface"),
      background=me.theme_var("surface-container-lowest"),
      display="flex",
      flex_direction="column",
      height="100%",
      padding=me.Padding.all(15),
    )
  ):
    # This contains the chat messages that have been recorded. This takes 50fr.
    # This section can be replaced with other types of chat messages.

    # We set overflow to scroll so that the chat input will be fixed at the bottom.
    with me.box(style=me.Style(overflow_y="scroll", flex_grow=1)):
      for msg in state.output:
        # User chat message
        if msg.role == "user":
          with me.box(
            style=me.Style(
              background=me.theme_var("primary-container"),
              border_radius=12,
              padding=me.Padding.all(12),
              margin=me.Margin.symmetric(vertical=8, horizontal=20),
              display="flex",
              align_items="center",
              max_width="75%",
              box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
            )
          ):
            # User query
            me.markdown(
              msg.content,
              style=me.Style(
                color=me.theme_var("on-primary-container"),
                font_size=14,
                line_height="1.5",
              ),
            )
        else:
          # Bot chat message
          with me.box(
            style=me.Style(display="flex", gap=15, margin=me.Margin.all(20))
          ):
            # Bot avatar/icon box
            me.text(
              "B",
              style=me.Style(
                background=me.theme_var("secondary"),
                border_radius="50%",
                color=me.theme_var("on-secondary"),
                font_size=20,
                height=40,
                width="40px",
                text_align="center",
                line_height="1",
                padding=me.Padding(top=10),
                margin=me.Margin(top=16),
              ),
            )
            # Bot message response
            me.markdown(
              msg.content,
              style=me.Style(color=me.theme_var("on-surface")),
            )

    # This is for the basic chat input. This is the second row at 1fr.
    # This section can be replaced with other types of chat inputs.
    with me.box(
      style=me.Style(
        border_radius=16,
        padding=me.Padding.all(8),
        background=me.theme_var("surface-container-low"),
        display="flex",
        width="100%",
      )
    ):
      with me.box(
        style=me.Style(
          flex_grow=1,
        )
      ):
        me.native_textarea(
          key="chat_input",
          value=state.input,
          on_blur=on_chat_input,
          autosize=True,
          min_rows=4,
          placeholder="Enter your prompt",
          style=me.Style(
            color=me.theme_var("on-surface-variant"),
            padding=me.Padding(top=16, left=16),
            background=me.theme_var("surface-container-low"),
            outline="none",
            width="100%",
            overflow_y="auto",
            border=me.Border.all(
              me.BorderSide(style="none"),
            ),
          ),
        )
      with me.content_button(
        type="icon",
        on_click=on_click_submit_chat_msg,
        # If we're processing a message prevent new queries from being sent
        disabled=state.in_progress,
      ):
        me.icon("send")


def on_chat_input(e: me.InputBlurEvent):
  """Capture chat text input on blur."""
  state = me.state(State)
  state.input = e.value


def on_click_submit_chat_msg(e: me.ClickEvent):
  """Handles submitting a chat message."""
  state = me.state(State)
  if state.in_progress or not state.input:
    return
  input = state.input
  # Clear the text input.
  state.input = ""
  yield

  output = state.output
  if output is None:
    output = []
  output.append(ChatMessage(role="user", content=input))
  state.in_progress = True
  yield

  start_time = time.time()
  # Send user input and chat history to get the bot response.
  output_message = respond_to_chat(input, state.output)
  assistant_message = ChatMessage(role="bot")
  output.append(assistant_message)
  state.output = output
  for content in output_message:
    assistant_message.content += content
    # TODO: 0.25 is an abitrary choice. In the future, consider making this adjustable.
    if (time.time() - start_time) >= 0.25:
      start_time = time.time()
      yield

  state.in_progress = False
  me.focus_component(key="chat_input")
  yield


def respond_to_chat(input: str, history: list[ChatMessage]):
  """Displays random canned text.

  Edit this function to process messages with a real chatbot/LLM.
  """
  lines = [
    "Mesop is a Python-based UI framework designed to simplify web UI development for engineers without frontend experience.",
    "It leverages the power of the Angular web framework and Angular Material components, allowing rapid construction of web demos and internal tools.",
    "With Mesop, developers can enjoy a fast build-edit-refresh loop thanks to its hot reload feature, making UI tweaks and component integration seamless.",
    "Deployment is straightforward, utilizing standard HTTP technologies.",
    "Mesop's component library aims for comprehensive Angular Material component coverage, enhancing UI flexibility and composability.",
    "It supports custom components for specific use cases, ensuring developers can extend its capabilities to fit their unique requirements.",
    "Mesop's roadmap includes expanding its component library and simplifying the onboarding processs.",
  ]
  for line in random.sample(lines, random.randint(3, len(lines) - 1)):
    yield line + " "
