import mesop as me
from chat_pad_components.foo import foo
from chat_pad_components import gemini
from chat_pad_components.data_model import ChatMessage

ROOT_BOX_STYLE = me.Style(
  background="#e7f2ff",
  height="100%",
  font_family="Inter",
  display="flex",
  flex_direction="column",
)

darker_bg_color = "#b9e1ff"


@me.page(
  path="/chat_pad",
  stylesheets=[
    "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
  ],
)
def page():
  with me.box(style=ROOT_BOX_STYLE):
    header()
    with me.box(
      style=me.Style(
        width="min(680px, 100%)",
        margin=me.Margin.symmetric(
          horizontal="auto",
          vertical=36,
        ),
      )
    ):
      me.text(
        "Chat with a scratch pad on the side",
        style=me.Style(
          font_size=20,
          margin=me.Margin(
            bottom=24,
          ),
        ),
      )
      examples_row()
      chat_input()
    # foo()


EXAMPLES = [
  "Create a file-lock in Python",
  "Write an email to Congress to have free milk for all",
  "Make a nice box shadow in CSS",
]


def examples_row():
  with me.box(
    style=me.Style(
      display="flex", flex_direction="row", gap=16, margin=me.Margin(bottom=24)
    )
  ):
    for i in EXAMPLES:
      example(i)


def example(text: str):
  with me.box(
    key=text,
    on_click=click_example,
    style=me.Style(
      cursor="pointer",
      background=darker_bg_color,
      width="215px",
      height=160,
      font_weight=500,
      line_height="1.5",
      padding=me.Padding.all(16),
      border_radius=16,
      border=me.Border.all(me.BorderSide(width=1, color="blue", style="none")),
    ),
  ):
    me.text(text)


def click_example(e: me.ClickEvent):
  state = me.state(State)
  state.input = e.key


def header():
  def navigate_home(e: me.ClickEvent):
    me.navigate("/chat_pad")
    state = me.state(State)
    state.messages = []

  with me.box(
    on_click=navigate_home,
    style=me.Style(
      cursor="pointer",
      padding=me.Padding.all(16),
    ),
  ):
    me.text(
      "ChatPad",
      style=me.Style(
        font_weight=500,
        font_size=24,
        color="#3D3929",
        letter_spacing="0.3px",
      ),
    )


def chat_input():
  state = me.state(State)
  with me.box(
    style=me.Style(
      border_radius=16,
      padding=me.Padding.all(8),
      background="white",
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
        value=state.input,
        autosize=True,
        min_rows=4,
        max_rows=8,
        placeholder="Enter a prompt",
        on_blur=on_blur,
        style=me.Style(
          padding=me.Padding(top=16, left=16),
          outline="none",
          width="100%",
          overflow_y="auto",
          border=me.Border.all(
            me.BorderSide(style="none"),
          ),
        ),
      )
    with me.content_button(type="icon", on_click=click_send):
      me.icon("send")


@me.stateclass
class State:
  input: str
  messages: list[ChatMessage]


def on_blur(e: me.InputEvent):
  state = me.state(State)
  state.input = e.value


def click_send(e: me.ClickEvent):
  yield from send_prompt()


def send_prompt():
  state = me.state(State)
  if not len(state.messages):
    me.navigate("/chat_pad/conversation")
  history = state.messages[:]
  state.messages.append(ChatMessage(role="user", content=state.input))
  input = state.input
  state.input = ""
  state.messages.append(ChatMessage(role="model", in_progress=True))
  yield
  me.scroll_into_view(key="end_of_messages")
  print("history", history)
  for chunk in gemini.send_prompt(input, history):
    state.messages[-1].content += chunk.text
    yield
  state.messages[-1].in_progress = False
  yield


@me.page(path="/chat_pad/conversation")
def conversation_page():
  state = me.state(State)
  with me.box(style=ROOT_BOX_STYLE):
    header()
    with me.box(
      style=me.Style(
        flex_grow=1,
        width="min(680px, 100%)",
        margin=me.Margin.symmetric(horizontal="auto"),
        padding=me.Padding.symmetric(horizontal=16),
        overflow_y="auto",
      )
    ):
      for message in state.messages:
        if message.role == "user":
          user_message(message.content)
        else:
          model_message(message)
      if state.messages:
        me.box(
          key="end_of_messages",
          style=me.Style(
            margin=me.Margin(
              bottom="50vh" if state.messages[-1].in_progress else 0
            )
          ),
        )
    with me.box(
      style=me.Style(
        display="flex",
        justify_content="center",
      )
    ):
      with me.box(
        style=me.Style(
          width="min(680px, 100%)",
          padding=me.Padding(top=24, bottom=24),
        )
      ):
        chat_input()


def user_message(content: str):
  with me.box(
    style=me.Style(
      background=darker_bg_color,
      padding=me.Padding.all(16),
      margin=me.Margin.symmetric(vertical=16),
      border_radius=16,
    )
  ):
    me.text(content)


def model_message(message: ChatMessage):
  with me.box(
    style=me.Style(
      background="#fff",
      padding=me.Padding.all(16),
      border_radius=16,
      margin=me.Margin.symmetric(vertical=16),
    )
  ):
    me.markdown(message.content)
    if message.in_progress:
      me.progress_spinner()
