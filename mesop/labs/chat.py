import time
from dataclasses import dataclass
from typing import Callable, Generator, Literal

import mesop as me

Role = Literal["user", "assistant"]

_ROLE_USER = "user"
_ROLE_ASSISTANT = "assistant"

_BOT_USER_DEFAULT = "mesop-bot"

_COLOR_BACKGROUND = me.theme_var("background")
_COLOR_CHAT_BUBBLE_YOU = me.theme_var("surface-container-low")
_COLOR_CHAT_BUBBLE_BOT = me.theme_var("secondary-container")

_DEFAULT_PADDING = me.Padding.all(20)
_DEFAULT_BORDER_SIDE = me.BorderSide(
  width="1px", style="solid", color=me.theme_var("secondary-fixed")
)

_LABEL_BUTTON = "send"
_LABEL_BUTTON_IN_PROGRESS = "pending"
_LABEL_INPUT = "Enter your prompt"

_STYLE_APP_CONTAINER = me.Style(
  background=_COLOR_BACKGROUND,
  display="grid",
  height="100vh",
  grid_template_columns="repeat(1, 1fr)",
)
_STYLE_TITLE = me.Style(padding=me.Padding(left=10))
_STYLE_CHAT_BOX = me.Style(
  height="100%",
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
  font_size="13px",
  padding=me.Padding(left=15, right=15, bottom=5),
)
_STYLE_CHAT_BUBBLE_PLAINTEXT = me.Style(margin=me.Margin.symmetric(vertical=15))


def _make_style_chat_ui_container(has_title: bool) -> me.Style:
  """Generates styles for chat UI container depending on if there is a title or not.

  Args:
    has_title: Whether the Chat UI is display a title or not.
  """
  return me.Style(
    display="grid",
    grid_template_columns="repeat(1, 1fr)",
    grid_template_rows="1fr 14fr 1fr" if has_title else "5fr 1fr",
    margin=me.Margin.symmetric(vertical=0, horizontal="auto"),
    width="min(1024px, 100%)",
    height="100vh",
    background=_COLOR_BACKGROUND,
    box_shadow=(
      "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
    ),
    padding=me.Padding(top=20, left=20, right=20),
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


def _make_chat_bubble_style(role: Role) -> me.Style:
  """Generates styles for chat bubble.

  Args:
    role: Chat bubble background color depends on the role
  """
  background = (
    _COLOR_CHAT_BUBBLE_YOU if role == _ROLE_USER else _COLOR_CHAT_BUBBLE_BOT
  )
  return me.Style(
    width="80%",
    font_size="16px",
    line_height="1.5",
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


@dataclass(kw_only=True)
class ChatMessage:
  """Chat message metadata."""

  role: Role = "user"
  content: str = ""


@me.stateclass
class State:
  input: str
  output: list[ChatMessage]
  in_progress: bool = False


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


def chat(
  transform: Callable[
    [str, list[ChatMessage]], Generator[str, None, None] | str
  ],
  *,
  title: str | None = None,
  bot_user: str = _BOT_USER_DEFAULT,
):
  """Creates a simple chat UI which takes in a prompt and chat history and returns a
  response to the prompt.

  This function creates event handlers for text input and output operations
  using the provided function `transform` to process the input and generate the output.

  Args:
    transform: Function that takes in a prompt and chat history and returns a response to the prompt.
    title: Headline text to display at the top of the UI.
    bot_user: Name of your bot / assistant.
  """
  state = me.state(State)

  def on_click_submit(e: me.ClickEvent):
    yield from submit()

  def on_input_enter(e: me.InputEnterEvent):
    state = me.state(State)
    state.input = e.value
    yield from submit()

  def submit():
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
    yield

    me.scroll_into_view(key="scroll-to")
    time.sleep(0.15)
    yield

    start_time = time.time()
    output_message = transform(input, state.output)
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

  def toggle_theme(e: me.ClickEvent):
    if me.theme_brightness() == "light":
      me.set_theme_mode("dark")
    else:
      me.set_theme_mode("light")

  with me.box(style=_STYLE_APP_CONTAINER):
    with me.content_button(
      type="icon",
      style=me.Style(position="absolute", right=4, top=8),
      on_click=toggle_theme,
    ):
      me.icon("light_mode" if me.theme_brightness() == "dark" else "dark_mode")
    with me.box(style=_make_style_chat_ui_container(bool(title))):
      if title:
        me.text(title, type="headline-5", style=_STYLE_TITLE)
      with me.box(style=_STYLE_CHAT_BOX):
        for msg in state.output:
          with me.box(style=_make_style_chat_bubble_wrapper(msg.role)):
            if msg.role == _ROLE_ASSISTANT:
              me.text(bot_user, style=_STYLE_CHAT_BUBBLE_NAME)
            with me.box(style=_make_chat_bubble_style(msg.role)):
              if msg.role == _ROLE_USER:
                me.text(msg.content, style=_STYLE_CHAT_BUBBLE_PLAINTEXT)
              else:
                me.markdown(msg.content)

        if state.in_progress:
          with me.box(key="scroll-to", style=me.Style(height=300)):
            pass

      with me.box(style=_STYLE_CHAT_INPUT_BOX):
        with me.box(style=me.Style(flex_grow=1)):
          me.input(
            label=_LABEL_INPUT,
            # Workaround: update key to clear input.
            key=f"{len(state.output)}",
            on_blur=on_blur,
            on_enter=on_input_enter,
            style=_STYLE_CHAT_INPUT,
          )
        with me.content_button(
          color="primary",
          type="flat",
          disabled=state.in_progress,
          on_click=on_click_submit,
          style=_STYLE_CHAT_BUTTON,
        ):
          me.icon(
            _LABEL_BUTTON_IN_PROGRESS if state.in_progress else _LABEL_BUTTON
          )
