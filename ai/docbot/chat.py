import re
import time
from dataclasses import dataclass, field
from typing import Generator, Literal

from docs_index import ask

import mesop as me
import mesop.labs as mel

# def ask(message: str):
#   yield "Hello, world![1]"
#   time.sleep(0.2)
#   yield "\nAnd More[2]"
#   time.sleep(0.2)
#   yield """Citations:

# 1. [Foo](https://foo.com)
# 2. [Bar](https://bar.com)
# 3. [Baz](https://baz.com)
# """


def on_load(e: me.LoadEvent):
  state = me.state(State)
  me.set_theme_mode("system")
  yield
  me.focus_component(key=f"input-{len(state.output)}")
  yield


@me.page(
  on_load=on_load,
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
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


def _make_style_chat_ui_container(has_title: bool) -> me.Style:
  """Generates styles for chat UI container depending on if there is a title or not.

  Args:
    has_title: Whether the Chat UI is display a title or not.
  """
  return me.Style(
    flex_grow=1,
    display="grid",
    grid_template_columns="repeat(1, 1fr)",
    grid_template_rows="1fr 14fr 1fr" if has_title else "5fr 1fr",
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


@me.stateclass
class State:
  input: str
  output: list[ChatMessage]
  citations: list[Citation]
  in_progress: bool = False


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


EXAMPLES = [
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
    # TODO: 0.25 is an abitrary choice. In the future, consider making this adjustable.
    if (time.time() - start_time) >= 0.25:
      start_time = time.time()
      print("transform_to_chunks")
      # transform assistant message into chunks
      transform_to_chunks(assistant_message)
      yield
  transform_to_chunks(assistant_message)
  state.in_progress = False
  me.focus_component(key=f"input-{len(state.output)}")
  yield


# TODO: handle the case where [4,5]
def transform_to_chunks(message: ChatMessage):
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
      # If it's a citation, add it to the current citations
      # current_citations.append(int(chunk))
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
  message.content = ""
  print("message.chunks", message.chunks)


def map_citation_numbers(citation_numbers: list[int]) -> list[int]:
  print("map_citation_numbers", citation_numbers)
  print("state.citations", me.state(State).citations)
  state = me.state(State)
  new_citation_numbers: set[int] = set()
  for citation_number in citation_numbers:
    for citation in state.citations:
      if citation_number in citation.original_numbers:
        new_citation_numbers.add(citation.number)
        break

    # raise ValueError(f"Citation number {citation_number} not found")
  print("new_citation_numbers", new_citation_numbers)
  return list(new_citation_numbers)


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
        # padding=me.Padding(top=30),
        display="flex",
        flex_direction="row",
        padding=me.Padding.all(8),
        background=me.theme_var("background"),
        # display="flex",
        width="100%",
        border=me.Border.all(
          me.BorderSide(width=0, style="solid", color="black")
        ),
        box_shadow="0 10px 20px #0000000a, 0 2px 6px #0000000a, 0 0 1px #0000000a",
      )
    ):
      with me.box(style=me.Style(flex_grow=1)):
        me.native_textarea(
          # appearance="outline",
          placeholder=_LABEL_INPUT,
          # Workaround: update key to clear input.
          key=f"input-{len(state.output)}",
          on_blur=on_blur,
          on_input=on_input,
          # on_enter=on_input_enter,
          min_rows=3,
          autosize=True,
          style=me.Style(
            # height="120px",
            # font_family="monospace",
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

    with me.box(style=_make_style_chat_ui_container(bool(title))):
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
            for example in EXAMPLES:
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
                # background=background,
                border_radius="15px",
                padding=me.Padding(right=15, left=15, bottom=3),
                margin=me.Margin(bottom=10),
                # border=me.Border(
                #   left=_DEFAULT_BORDER_SIDE,
                #   right=_DEFAULT_BORDER_SIDE,
                #   top=_DEFAULT_BORDER_SIDE,
                #   bottom=_DEFAULT_BORDER_SIDE,
                # ),
              )
            ):
              if msg.role == _ROLE_USER:
                me.text(
                  msg.content, style=me.Style(margin=me.Margin(bottom=16))
                )
              else:
                for chunk in msg.chunks:
                  me.text(
                    chunk.content,
                    style=me.Style(white_space="pre-wrap", display="inline"),
                  )
                  if chunk.citation_numbers:
                    with me.box(
                      style=me.Style(
                        display="inline-flex",
                        flex_direction="row",
                        gap=4,
                        margin=me.Margin.symmetric(horizontal=6),
                      )
                    ):
                      for citation_number in chunk.citation_numbers:
                        citation_tooltip(citation_number)
                  # me.text(msg.content, style=me.Style(white_space="pre"))
                with me.box(
                  style=me.Style(
                    padding=me.Padding(top=16),
                    display="flex",
                    flex_direction="column",
                    gap=16,
                  ),
                ):
                  for citation in state.citations:
                    with citation_box(url=citation.url):
                      citation_content(citation)


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
    url = source_node.node.metadata.get("url", "")
    breadcrumbs = url.split("https://google.github.io/mesop/")[-1].split("/")
    title = source_node.node.metadata.get("title", "")
    citations.append(
      Citation(url=url, breadcrumbs=breadcrumbs, title=title, number=i + 1)
    )

  me.state(State).citations = dedupe_citations(citations)
  yield from response_stream.response_gen
  # return stubbed_transform(message, history)


def dedupe_citations(citations: list[Citation]) -> list[Citation]:
  # dedupe citations by url and group the number into original_nubmers
  deduped_citations: dict[str, Citation] = {}
  for citation in citations:
    if citation.url in deduped_citations:
      deduped_citations[citation.url].original_numbers.append(citation.number)
    else:
      deduped_citations[citation.url] = citation
      deduped_citations[citation.url].original_numbers = [citation.number]

  result = list(deduped_citations.values())
  for i, citation in enumerate(result):
    citation.number = i + 1

  return result


def stubbed_transform(
  message: str, history: list[ChatMessage]
) -> Generator[str, None, None]:
  me.state(State).citations = dedupe_citations(
    [
      Citation(
        url="https://foo.com", title="Foo", breadcrumbs=["Foo", "Bar"], number=1
      ),
      Citation(
        url="https://bar.com", title="Bar", breadcrumbs=["Foo", "Bar"], number=2
      ),
      Citation(
        url="https://baz.com", title="Baz", breadcrumbs=["Foo", "Bar"], number=3
      ),
      Citation(
        url="https://baz.com", title="Baz", breadcrumbs=["Foo", "Bar"], number=4
      ),
    ]
  )

  # response_stream = ask(message)
  # for text in response_stream.response_gen:
  yield from ["Hello, world![3, 4, 1]", "And More[2]"]
  # source_urls: set[str] = set()

  # for source_node in response_stream.source_nodes:
  #   url = source_node.node.metadata.get("url", "")
  #   if url:
  #     source_urls.add(url)
  # source_urls = set(["https://foo.com", "https://bar.com", "https://baz.com"])


#   yield f"""
# __Sources:__

# {NEWLINE.join([f"- [{url}]({url})" for url in source_urls])}
#   """
