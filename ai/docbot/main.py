import random
import re
import time
import urllib
from dataclasses import dataclass, field
from typing import Generator, Literal

from docs_index import ask

import mesop as me
import mesop.labs as mel


def on_load(e: me.LoadEvent):
  state = me.state(State)
  state.examples = random.sample(EXAMPLES, 3)
  if "prompt" in me.query_params:
    state.initial_input = me.query_params["prompt"]
  me.set_theme_mode("system")
  yield
  me.focus_component(key=f"input-{len(state.output)}")
  yield


@me.page(
  on_load=on_load,
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ],
    allowed_iframe_parents=[
      "https://huggingface.co",
      "https://google.github.io",
    ],
  ),
  title="Mesop Docs Chat",
)
def page():
  return chat()


Role = Literal["user", "assistant"]

_ROLE_USER = "user"
_ROLE_ASSISTANT = "assistant"

_BOT_USER_DEFAULT = "Mesop Docs Bot"

_COLOR_BACKGROUND = me.theme_var("background")

_DEFAULT_PADDING = me.Padding.all(12)

_LABEL_BUTTON = "send"
_LABEL_BUTTON_IN_PROGRESS = "pending"
_LABEL_INPUT = "Ask Mesop Docs Bot"

_STYLE_APP_CONTAINER = me.Style(
  background=_COLOR_BACKGROUND,
  display="flex",
  flex_direction="column",
  height="100%",
)
_STYLE_TITLE = me.Style(padding=me.Padding(left=10))
_STYLE_CHAT_BOX = me.Style(
  height="100%",
  overflow_y="scroll",
  padding=_DEFAULT_PADDING,
  background=me.theme_var("background"),
)

_STYLE_CHAT_BUTTON = me.Style(margin=me.Margin(top=8, left=8))
_STYLE_CHAT_BUBBLE_NAME = me.Style(
  font_weight="bold",
  font_size="13px",
  padding=me.Padding(left=15, right=15, bottom=5),
)


def _make_style_chat_ui_container() -> me.Style:
  return me.Style(
    flex_grow=1,
    display="grid",
    grid_template_columns="repeat(1, 1fr)",
    grid_template_rows="5fr 1fr",
    margin=me.Margin.symmetric(vertical=0, horizontal="auto"),
    width="min(100%)",
    background=_COLOR_BACKGROUND,
    box_shadow=(
      "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
    ),
    padding=me.Padding(top=3, left=12, right=12),
  )


@dataclass(kw_only=True)
class Chunk:
  content: str = ""
  citation_numbers: list[int] = field(default_factory=list)


@dataclass(kw_only=True)
class ChatMessage:
  """Chat message metadata."""

  role: Role = "user"
  content: str = ""
  chunks: list[Chunk] = field(default_factory=list)


@dataclass(kw_only=True)
class Citation:
  number: int = 0
  original_numbers: list[int] = field(default_factory=list)
  url: str = ""
  title: str = ""
  breadcrumbs: list[str] = field(default_factory=list)
  content: str = ""


@me.stateclass
class State:
  input: str
  initial_input: str
  output: list[ChatMessage]
  citations: list[Citation]
  in_progress: bool = False
  examples: list[str]


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


mesop_questions = [
  "How do I test a Mesop application?",
  "What components are available in Mesop?",
  "How can I reset a text input field in Mesop?",
  "Show me how to style a component in Mesop",
  "Create a multi-page app using Mesop",
  "Is it possible to create custom components in Mesop?",
  "Implement authentication in a Mesop app",
  "How do I call an API from a Mesop application?",
  "What's the process for deploying a Mesop app?",
  "Optimize performance in a Mesop application",
  "Implement a datepicker in Mesop",
  "Can I use JavaScript libraries with Mesop?",
  "Implement real-time updates in a Mesop app",
  "Stream UI updates from an LLM API in Mesop",
  "Debug a Mesop application",
  "Is Mesop ready for production use?",
  "Implement form validation in Mesop",
  "Create a mobile-friendly Mesop app",
  "Handle asynchronous operations in Mesop",
  "Implement dark mode in a Mesop application",
  "Add keyboard shortcuts to a Mesop app",
  "Implement drag and drop functionality in Mesop",
  "Create an infinite scroll feature in Mesop",
  "How to make a row of components in Mesop",
  "Add tooltips to Mesop components",
  "Render a pandas DataFrame in a Mesop app",
  "Add charts to a Mesop application",
  "Create a table component in Mesop",
  "Handle file uploads in a Mesop app",
  "Use command-line flags with a Mesop application",
  "Create a clickable link in Mesop",
  "Implement a download link in a Mesop app",
]

EXAMPLES = [
  *mesop_questions,
  "How do I create a streaming chat UI?",
  "How do I install Mesop?",
  "How is Mesop different from other UI frameworks?",
]


def on_click_submit(e: me.ClickEvent) -> Generator[None, None, None]:
  yield from submit()


def on_input(e: me.InputEvent) -> Generator[None, None, None]:
  state = me.state(State)
  if not e.value.endswith("\n"):
    return
  state.input = e.value
  yield from submit()
  me.focus_component(key=f"input-{len(state.output)}")
  yield


def submit():
  state = me.state(State)
  if state.in_progress or not state.input:
    return
  input = state.input
  state.input = ""
  yield

  state.output = []
  output = state.output
  output.append(ChatMessage(role=_ROLE_USER, content=input))
  state.in_progress = True
  yield

  start_time = time.time()
  output_message = transform(input, state.output)
  assistant_message = ChatMessage(role=_ROLE_ASSISTANT)
  output.append(assistant_message)
  state.output = output

  for content in output_message:
    assistant_message.content += content

    if (time.time() - start_time) >= 0.35:
      start_time = time.time()
      transform_to_chunks(assistant_message)
      yield
  transform_to_chunks(assistant_message)
  state.in_progress = False
  me.focus_component(key=f"input-{len(state.output)}")
  yield


# TODO: handle the case where [4,5]
def transform_to_chunks(message: ChatMessage):
  message.chunks = []
  # Split the message content into chunks based on citations
  chunks = re.split(r"(\[\d+(?:,\s*\d+)*\])", message.content)
  print("chunks'", chunks)
  # Initialize variables
  current_chunk = ""
  current_citations: list[int] = []

  # Process each chunk
  for chunk in chunks:
    print("chunk", chunk)
    if re.match(r"\[\d+(?:,\s*\d+)*\]", chunk):
      print("chunk is a citation")
      try:
        # Remove brackets and split by comma
        citation_numbers = [int(num.strip()) for num in chunk[1:-1].split(",")]
        current_citations.extend(citation_numbers)
      except Exception as e:
        print(f"Error: Unable to parse citation numbers - {e}")
    else:
      # If it's text content
      if current_chunk:
        # If there's existing content, create a new chunk
        message.chunks.append(
          Chunk(
            content=current_chunk,
            citation_numbers=map_citation_numbers(current_citations),
          )
        )
        current_chunk = ""
        current_citations = []
      # Add the new content
      current_chunk += chunk

  print("current_chunk", current_chunk)
  print("current_citations", current_citations)
  # Add the last chunk if there's any remaining content
  if current_chunk:
    message.chunks.append(
      Chunk(
        content=current_chunk,
        citation_numbers=map_citation_numbers(current_citations),
      )
    )

  # Clear the original content as it's now split into chunks
  print("message.chunks", message.chunks)


def map_citation_numbers(citation_numbers: list[int]) -> list[int]:
  return citation_numbers


def chat(
  title: str | None = None,
  bot_user: str = _BOT_USER_DEFAULT,
):
  state = me.state(State)

  def toggle_theme(e: me.ClickEvent):
    if me.theme_brightness() == "light":
      me.set_theme_mode("dark")
    else:
      me.set_theme_mode("light")

  with me.box(style=_STYLE_APP_CONTAINER):
    with me.content_button(
      type="icon",
      style=me.Style(position="absolute", left=8, top=12),
      on_click=toggle_theme,
    ):
      me.icon("light_mode" if me.theme_brightness() == "dark" else "dark_mode")
    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="row",
        padding=me.Padding.all(8),
        background=me.theme_var("background"),
        width="100%",
        border=me.Border.all(
          me.BorderSide(width=0, style="solid", color="black")
        ),
        box_shadow="0 10px 20px #0000000a, 0 2px 6px #0000000a, 0 0 1px #0000000a",
      )
    ):
      with me.box(style=me.Style(flex_grow=1)):
        me.native_textarea(
          value=state.initial_input,
          placeholder=_LABEL_INPUT,
          key=f"input-{len(state.output)}",
          on_blur=on_blur,
          on_input=on_input,
          min_rows=3,
          autosize=True,
          style=me.Style(
            color=me.theme_var("on-background"),
            padding=me.Padding(top=16, left=48),
            background=me.theme_var("background"),
            letter_spacing="0.07px",
            outline="none",
            width="100%",
            overflow_y="auto",
            border=me.Border.all(
              me.BorderSide(style="none"),
            ),
          ),
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

    with me.box(style=_make_style_chat_ui_container()):
      if title:
        me.text(title, type="headline-5", style=_STYLE_TITLE)
      with me.box(style=_STYLE_CHAT_BOX):
        if not state.output:
          me.text(
            "Welcome to Mesop Docs Bot! Ask me anything about Mesop.",
            style=me.Style(
              margin=me.Margin(bottom=24),
              font_weight=500,
            ),
          )
          with me.box(
            style=me.Style(
              display="flex",
              flex_direction="column",
              gap=24,
            )
          ):
            for example in state.examples:
              example_box(example)
        for msg in state.output:
          with me.box(
            style=me.Style(
              display="flex", flex_direction="column", align_items="start"
            )
          ):
            if msg.role == _ROLE_ASSISTANT:
              me.text(bot_user, style=_STYLE_CHAT_BUBBLE_NAME)
            else:
              me.text("You", style=_STYLE_CHAT_BUBBLE_NAME)
            with me.box(
              style=me.Style(
                width="100%",
                font_size="16px",
                line_height="1.5",
                border_radius="15px",
                padding=me.Padding(right=15, left=15, bottom=3),
                margin=me.Margin(bottom=10),
              )
            ):
              if msg.role == _ROLE_USER:
                me.text(
                  msg.content, style=me.Style(margin=me.Margin(bottom=16))
                )
              else:
                used_citation_numbers: set[int] = set()

                for chunk in msg.chunks:
                  me.text(
                    chunk.content,
                    style=me.Style(white_space="pre-wrap", display="inline"),
                  )
                  if chunk.citation_numbers:
                    print(
                      "chunk.content",
                      chunk.content,
                      "chunk.citation_numbers",
                      me.state(State).citations[chunk.citation_numbers[0] - 1],
                    )
                    with me.box(
                      style=me.Style(
                        display="inline-flex",
                        flex_direction="row",
                        gap=4,
                        margin=me.Margin.symmetric(horizontal=6),
                      )
                    ):
                      for citation_number in chunk.citation_numbers:
                        used_citation_numbers.add(citation_number)

                        citation_tooltip(
                          get_citation_number(
                            citation_number, used_citation_numbers
                          )
                        )

                with me.box(
                  style=me.Style(
                    padding=me.Padding(top=16),
                    display="flex",
                    flex_direction="column",
                    gap=16,
                  ),
                ):
                  for citation in state.citations:
                    if citation.number in used_citation_numbers:
                      with citation_box(url=citation.url):
                        citation_content(
                          Citation(
                            url=citation.url,
                            title=citation.title,
                            breadcrumbs=citation.breadcrumbs,
                            original_numbers=citation.original_numbers,
                            content=citation.content,
                            number=get_citation_number(
                              citation.number, used_citation_numbers
                            ),
                          )
                        )
                if not me.state(State).in_progress:
                  with me.box(
                    style=me.Style(
                      display="flex",
                      flex_direction="row",
                      gap=4,
                      margin=me.Margin(top=16),
                    )
                  ):
                    NEWLINE = "\n"
                    me.text("Is there an issue with this this response?")
                    me.link(
                      text="File an issue",
                      url="https://github.com/google/mesop/issues/new?assignees=&labels=bug,chatbot&projects=&title=Bad%20chatbot%20response&body="
                      + urllib.parse.quote(f"""
What was the issue with the chatbot response?

---
Original content:

__Prompt:__
{state.output[0].content}

__Response:__
{state.output[-1].content}

__Citations:__

{NEWLINE.join([f"1. {citation.url}" for citation in state.citations])}
"""),
                      style=me.Style(
                        color=me.theme_var("primary"),
                        text_decoration="none",
                      ),
                      open_in_new_tab=True,
                    )


def citation_tooltip(citation_number: int):
  state = me.state(State)
  with me.box(style=me.Style(display="inline-block")):
    with me.tooltip(
      message=state.citations[citation_number - 1].title,
      position="below",
    ):
      me.text(
        f"{citation_number}",
        style=me.Style(
          background=me.theme_var("surface-variant"),
          padding=me.Padding.symmetric(horizontal=5),
          border_radius="6px",
          font_weight=500,
        ),
      )


@mel.web_component(path="./citation.js")
def citation_box(
  *,
  url: str,
  key: str | None = None,
):
  return mel.insert_web_component(
    name="citation-component",
    key=key,
    properties={
      "url": url,
      "active": True,
    },
  )


def citation_content(citation: Citation):
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      padding=me.Padding.symmetric(vertical=8, horizontal=16),
      cursor="pointer",
    ),
  ):
    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="row",
        gap=4,
        align_items="start",
      )
    ):
      me.text(
        f"{citation.number}", style=me.Style(font_weight=500, font_size=18)
      )
      me.icon(
        icon="description",
        style=me.Style(font_size=20, padding=me.Padding(top=3, left=3)),
      )

      me.text(citation.title)
    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="row",
        gap=8,
        font_size="14px",
        font_weight=500,
      )
    ):
      for breadcrumb in citation.breadcrumbs:
        me.text(breadcrumb)
        if breadcrumb != citation.breadcrumbs[-1]:
          me.text(" > ")


def example_box(example: str):
  with me.box(
    style=me.Style(
      background=me.theme_var("secondary-container"),
      border_radius="12px",
      padding=me.Padding(left=16, right=16, top=16, bottom=16),
      cursor="pointer",
    ),
    key=example,
    on_click=on_click_example,
  ):
    me.text(example)


def on_click_example(e: me.ClickEvent) -> Generator[None, None, None]:
  state = me.state(State)
  state.input = e.key
  yield from submit()


def transform(
  message: str, history: list[ChatMessage]
) -> Generator[str, None, None]:
  response_stream = ask(message)
  citations: list[Citation] = []

  for i, source_node in enumerate(response_stream.source_nodes):
    url: str = source_node.node.metadata.get("url", "")
    breadcrumbs = url.split("https://google.github.io/mesop/")[-1].split("/")
    title = source_node.node.metadata.get("title", "")
    content_lines = source_node.node.get_content().split("\n")

    for line in content_lines[2:]:
      if line and not line.startswith("```"):
        break

    fragment: str = (
      "#:~:text="
      + urllib.parse.quote(content_lines[1])
      + ",-"
      # Just take the first two words of the line to avoid
      # mismatching (e.g. URLs).
      + urllib.parse.quote(" ".join(line.split(" ")[:2]))
    )
    citations.append(
      Citation(
        url=url + fragment,
        breadcrumbs=breadcrumbs,
        title=title,
        number=i + 1,
      )
    )

  me.state(State).citations = citations
  yield from response_stream.response_gen


def get_citation_number(
  citation_number: int, used_citation_numbers: set[int]
) -> int:
  number = 0
  for n in used_citation_numbers:
    number += 1  # noqa: SIM113
    if n == citation_number:
      return number
  raise ValueError(f"Citation number {citation_number} not found")
