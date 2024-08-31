import random
import time
from dataclasses import dataclass
from typing import Literal

import mesop as me

Role = Literal["user", "assistant"]


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
  rewrite: str
  rewrite_message_index: int
  preview_rewrite: str
  preview_original: str
  modal_open: bool


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/llm_rewriter",
  title="LLM Rewriter",
)
def page():
  state = me.state(State)

  # Modal
  with me.box(style=_make_modal_background_style(state.modal_open)):
    with me.box(style=_STYLE_MODAL_CONTAINER):
      with me.box(style=_STYLE_MODAL_CONTENT):
        me.textarea(
          label="Rewrite",
          style=_STYLE_INPUT_WIDTH,
          value=state.rewrite,
          on_input=on_rewrite_input,
        )
        with me.box():
          me.button(
            "Submit Rewrite",
            color="primary",
            type="flat",
            on_click=on_click_submit_rewrite,
          )
          me.button(
            "Cancel",
            on_click=on_click_cancel_rewrite,
          )
        with me.box(style=_STYLE_PREVIEW_CONTAINER):
          with me.box(style=_STYLE_PREVIEW_ORIGINAL):
            me.text("Original Message", type="headline-6")
            me.markdown(state.preview_original)

          with me.box(style=_STYLE_PREVIEW_REWRITE):
            me.text("Preview Rewrite", type="headline-6")
            me.markdown(state.preview_rewrite)

  # Chat UI
  with me.box(style=_STYLE_APP_CONTAINER):
    me.text(_TITLE, type="headline-5", style=_STYLE_TITLE)
    with me.box(style=_STYLE_CHAT_BOX):
      for index, msg in enumerate(state.output):
        with me.box(
          style=_make_style_chat_bubble_wrapper(msg.role),
          key=f"msg-{index}",
          on_click=on_click_rewrite_msg,
        ):
          if msg.role == _ROLE_ASSISTANT:
            me.text(
              _display_username(_BOT_USER_DEFAULT, msg.edited),
              style=_STYLE_CHAT_BUBBLE_NAME,
            )
          with me.box(style=_make_chat_bubble_style(msg.role, msg.edited)):
            if msg.role == _ROLE_USER:
              me.text(msg.content, style=_STYLE_CHAT_BUBBLE_PLAINTEXT)
            else:
              me.markdown(msg.content)
              with me.tooltip(message="Rewrite response"):
                me.icon(icon="edit_note")

      if state.in_progress:
        with me.box(key="scroll-to", style=me.Style(height=250)):
          pass
    with me.box(style=_STYLE_CHAT_INPUT_BOX):
      with me.box(style=me.Style(flex_grow=1)):
        me.input(
          label=_LABEL_INPUT,
          # Workaround: update key to clear input.
          key=f"input-{len(state.output)}",
          on_input=on_chat_input,
          on_enter=on_click_submit_chat_msg,
          style=_STYLE_CHAT_INPUT,
        )
      with me.content_button(
        color="primary",
        type="flat",
        disabled=state.in_progress,
        on_click=on_click_submit_chat_msg,
        style=_STYLE_CHAT_BUTTON,
      ):
        me.icon(
          _LABEL_BUTTON_IN_PROGRESS if state.in_progress else _LABEL_BUTTON
        )


# Event Handlers


def on_chat_input(e: me.InputEvent):
  """Capture chat text input."""
  state = me.state(State)
  state.input = e.value


def on_rewrite_input(e: me.InputEvent):
  """Capture rewrite text input."""
  state = me.state(State)
  state.preview_rewrite = e.value


def on_click_rewrite_msg(e: me.ClickEvent):
  """Shows rewrite modal when a message is clicked.

  Edit this function to persist rewritten messages.
  """
  state = me.state(State)
  index = int(e.key.replace("msg-", ""))
  message = state.output[index]
  if message.role == _ROLE_USER or state.in_progress:
    return
  state.modal_open = True
  state.rewrite = message.content
  state.rewrite_message_index = index
  state.preview_original = message.content
  state.preview_rewrite = message.content


def on_click_submit_rewrite(e: me.ClickEvent):
  """Submits rewrite message."""
  state = me.state(State)
  state.modal_open = False
  message = state.output[state.rewrite_message_index]
  if message.content != state.preview_rewrite:
    message.content = state.preview_rewrite
    message.edited = True
  state.rewrite_message_index = 0
  state.rewrite = ""
  state.preview_original = ""
  state.preview_rewrite = ""


def on_click_cancel_rewrite(e: me.ClickEvent):
  """Hides rewrite modal."""
  state = me.state(State)
  state.modal_open = False
  state.rewrite_message_index = 0
  state.rewrite = ""
  state.preview_original = ""
  state.preview_rewrite = ""


def on_click_submit_chat_msg(e: me.ClickEvent | me.InputEnterEvent):
  """Handles submitting a chat message."""
  state = me.state(State)
  if state.in_progress or not state.input:
    return
  input = state.input
  state.input = ""
  yield

  output = state.output
  if output is None:
    output = []
  output.append(ChatMessage(role=_ROLE_USER, content=input))
  state.in_progress = True
  me.scroll_into_view(key="scroll-to")
  yield

  start_time = time.time()
  output_message = respond_to_chat(input, state.output)
  assistant_message = ChatMessage(role=_ROLE_ASSISTANT)
  output.append(assistant_message)
  state.output = output
  for content in output_message:
    assistant_message.content += content
    # TODO: 0.25 is an abitrary choice. In the future, consider making this adjustable.
    if (time.time() - start_time) >= 0.25:
      start_time = time.time()
      yield

  state.in_progress = False
  yield


# Transform function for processing chat messages.


def respond_to_chat(input: str, history: list[ChatMessage]):
  """Displays random canned text.

  Edit this function to process messages with a real chatbot/LLM.
  """
  lines = [
    (
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
      "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    ),
    "Laoreet sit amet cursus sit amet dictum sit amet.",
    "At lectus urna duis convallis.",
    "A pellentesque sit amet porttitor eget.",
    "Mauris nunc congue nisi vitae suscipit tellus mauris a diam.",
    "Aliquet lectus proin nibh nisl condimentum id.",
    "Integer malesuada nunc vel risus commodo viverra maecenas accumsan.",
    "Tempor id eu nisl nunc mi.",
    "Id consectetur purus ut faucibus pulvinar.",
    "Mauris pharetra et ultrices neque ornare.",
    "Facilisis magna etiam tempor orci.",
    "Mauris pharetra et ultrices neque.",
    "Sit amet facilisis magna etiam tempor orci.",
    "Amet consectetur adipiscing elit pellentesque habitant morbi tristique.",
    "Egestas erat imperdiet sed euismod.",
    "Tincidunt praesent semper feugiat nibh sed pulvinar proin gravida.",
    "Habitant morbi tristique senectus et netus et malesuada.",
  ]
  for line in random.sample(lines, random.randint(3, len(lines) - 1)):
    time.sleep(0.25)
    yield line + " "


# Constants

_TITLE = "LLM Rewriter"

_ROLE_USER = "user"
_ROLE_ASSISTANT = "assistant"

_BOT_USER_DEFAULT = "mesop-bot"


# Styles

_COLOR_BACKGROUND = "#fff"
_COLOR_CHAT_BUBBLE_YOU = "#f2f2f2"
_COLOR_CHAT_BUBBLE_BOT = "#ebf3ff"
_COLOR_CHAT_BUUBBLE_EDITED = "#f2ebff"

_DEFAULT_PADDING = me.Padding.all(20)
_DEFAULT_BORDER_SIDE = me.BorderSide(
  width="1px", style="solid", color="#ececec"
)

_LABEL_BUTTON = "send"
_LABEL_BUTTON_IN_PROGRESS = "pending"
_LABEL_INPUT = "Enter your prompt"

_STYLE_INPUT_WIDTH = me.Style(width="100%")

_STYLE_APP_CONTAINER = me.Style(
  background=_COLOR_BACKGROUND,
  display="flex",
  flex_direction="column",
  height="100%",
  margin=me.Margin.symmetric(vertical=0, horizontal="auto"),
  width="min(1024px, 100%)",
  box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
  padding=me.Padding(top=20, left=20, right=20),
)
_STYLE_TITLE = me.Style(padding=me.Padding(left=10))
_STYLE_CHAT_BOX = me.Style(
  flex_grow=1,
  overflow_y="scroll",
  padding=_DEFAULT_PADDING,
  margin=me.Margin(bottom=20),
  border_radius="10px",
  border=me.Border(
    left=_DEFAULT_BORDER_SIDE,
    right=_DEFAULT_BORDER_SIDE,
    top=_DEFAULT_BORDER_SIDE,
    bottom=_DEFAULT_BORDER_SIDE,
  ),
)
_STYLE_CHAT_INPUT = me.Style(width="100%")
_STYLE_CHAT_INPUT_BOX = me.Style(
  padding=me.Padding(top=30), display="flex", flex_direction="row"
)
_STYLE_CHAT_BUTTON = me.Style(margin=me.Margin(top=8, left=8))
_STYLE_CHAT_BUBBLE_NAME = me.Style(
  font_weight="bold",
  font_size="12px",
  padding=me.Padding(left=15, right=15, bottom=5),
)
_STYLE_CHAT_BUBBLE_PLAINTEXT = me.Style(margin=me.Margin.symmetric(vertical=15))

_STYLE_MODAL_CONTAINER = me.Style(
  background="#fff",
  margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
  width="min(1024px, 100%)",
  box_sizing="content-box",
  height="100%",
  overflow_y="scroll",
  box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"),
)

_STYLE_MODAL_CONTENT = me.Style(margin=me.Margin.all(20))

_STYLE_PREVIEW_CONTAINER = me.Style(
  display="grid",
  grid_template_columns="repeat(2, 1fr)",
)

_STYLE_PREVIEW_ORIGINAL = me.Style(color="#777", padding=_DEFAULT_PADDING)

_STYLE_PREVIEW_REWRITE = me.Style(
  background=_COLOR_CHAT_BUUBBLE_EDITED, padding=_DEFAULT_PADDING
)


def _make_style_chat_bubble_wrapper(role: Role) -> me.Style:
  """Generates styles for chat bubble position.

  Args:
    role: Chat bubble alignment depends on the role
  """
  align_items = "end" if role == _ROLE_USER else "start"
  return me.Style(
    display="flex",
    flex_direction="column",
    align_items=align_items,
  )


def _make_chat_bubble_style(role: Role, edited: bool) -> me.Style:
  """Generates styles for chat bubble.

  Args:
    role: Chat bubble background color depends on the role
    edited: Whether chat message was edited or not.
  """
  background = _COLOR_CHAT_BUBBLE_YOU
  if role == _ROLE_ASSISTANT:
    background = _COLOR_CHAT_BUBBLE_BOT
  if edited:
    background = _COLOR_CHAT_BUUBBLE_EDITED

  return me.Style(
    width="80%",
    font_size="13px",
    background=background,
    border_radius="15px",
    padding=me.Padding(right=15, left=15, bottom=3),
    margin=me.Margin(bottom=10),
    border=me.Border(
      left=_DEFAULT_BORDER_SIDE,
      right=_DEFAULT_BORDER_SIDE,
      top=_DEFAULT_BORDER_SIDE,
      bottom=_DEFAULT_BORDER_SIDE,
    ),
  )


def _make_modal_background_style(modal_open: bool) -> me.Style:
  """Makes style for modal background.

  Args:
    modal_open: Whether the modal is open.
  """
  return me.Style(
    display="block" if modal_open else "none",
    position="fixed",
    z_index=1000,
    width="100%",
    height="100%",
    overflow_x="auto",
    overflow_y="auto",
    background="rgba(0,0,0,0.4)",
  )


def _display_username(username: str, edited: bool = False) -> str:
  """Displays the username

  Args:
    username: Name of the user
    edited: Whether the message has been edited.
  """
  edited_text = " (edited)" if edited else ""
  return username + edited_text
