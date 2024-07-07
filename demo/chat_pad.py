from dataclasses import field
from enum import Enum

from chat_pad_components import claude, gemini
from chat_pad_components.data_model import ChatMessage
from chat_pad_components.dialog import dialog, dialog_actions

import mesop as me

ROOT_BOX_STYLE = me.Style(
  background="#e7f2ff",
  height="100%",
  font_family="Inter",
  display="flex",
  flex_direction="column",
)

darker_bg_color = "#b9e1ff"

STYLESHEETS = [
  "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]


class Models(Enum):
  GEMINI_1_5_FLASH = "Gemini 1.5 Flash"
  GEMINI_1_5_PRO = "Gemini 1.5 Pro"
  CLAUDE_3_5_SONNET = "Claude 3.5 Sonnet"


@me.stateclass
class State:
  is_model_picker_dialog_open: bool
  input: str
  messages_by_model: dict[str, list[ChatMessage]]
  models: list[str] = field(
    default_factory=lambda: [Models.GEMINI_1_5_FLASH.value]
  )


@me.stateclass
class ModelDialogState:
  selected_models: list[str]


def change_model_option(e: me.CheckboxChangeEvent):
  s = me.state(ModelDialogState)
  if e.checked:
    s.selected_models.append(e.key)
  else:
    s.selected_models.remove(e.key)


def model_picker_dialog():
  state = me.state(State)
  with dialog(state.is_model_picker_dialog_open):
    me.text("Pick a model")
    for model in Models:
      me.checkbox(
        key=model.value,
        label=model.value,
        checked=model.value in state.models,
        on_change=change_model_option,
        style=me.Style(
          display="flex",
          flex_direction="column",
          gap=4,
          padding=me.Padding(top=12),
        ),
      )
    with dialog_actions():
      me.button("Cancel", on_click=close_model_picker_dialog)
      me.button("Confirm", on_click=confirm_model_picker_dialog)


@me.page(path="/chat_pad", stylesheets=STYLESHEETS)
def page():
  model_picker_dialog()
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
        "Chat with multiple models at once",
        style=me.Style(
          font_size=20,
          margin=me.Margin(
            bottom=24,
          ),
        ),
      )
      examples_row()
      chat_input()


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
    state.messages_by_model = {}

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
      with me.box():
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
        with me.box(
          style=me.Style(
            display="flex",
            padding=me.Padding(left=12, bottom=12),
            cursor="pointer",
          ),
          on_click=switch_model,
        ):
          me.text(
            "Model:",
            style=me.Style(font_weight=500, padding=me.Padding(right=6)),
          )
          me.text(
            ", ".join(state.models),
            style=me.Style(),
          )
    with me.content_button(type="icon", on_click=send_prompt):
      me.icon("send")


def switch_model(e: me.ClickEvent):
  state = me.state(State)
  state.is_model_picker_dialog_open = True
  dialog_state = me.state(ModelDialogState)
  dialog_state.selected_models = state.models[:]


def close_model_picker_dialog(e: me.ClickEvent):
  state = me.state(State)
  state.is_model_picker_dialog_open = False


def confirm_model_picker_dialog(e: me.ClickEvent):
  dialog_state = me.state(ModelDialogState)
  state = me.state(State)
  state.is_model_picker_dialog_open = False
  state.models = dialog_state.selected_models


def on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value


def send_prompt(e: me.ClickEvent):
  state = me.state(State)
  if not len(state.messages_by_model.keys()):
    me.navigate("/chat_pad/conversation")
  input = state.input
  state.input = ""

  for model in state.models:
    if model not in state.messages_by_model:
      state.messages_by_model[model] = []
    messages = state.messages_by_model.get(model)
    assert messages is not None
    history = messages[:]
    messages.append(ChatMessage(role="user", content=input))
    messages.append(ChatMessage(role="model", in_progress=True))
    yield
    me.scroll_into_view(key="end_of_messages")
    if model == Models.GEMINI_1_5_FLASH.value:
      llm_response = gemini.send_prompt_flash(input, history)
    elif model == Models.GEMINI_1_5_PRO.value:
      llm_response = gemini.send_prompt_pro(input, history)
    elif model == Models.CLAUDE_3_5_SONNET.value:
      llm_response = claude.call_claude_sonnet(input, history)  # type: ignore
    else:
      raise Exception("Unhandled model", model)
    for chunk in llm_response:  # type: ignore
      messages[-1].content += chunk
      yield
    messages[-1].in_progress = False
    yield


@me.page(path="/chat_pad/conversation", stylesheets=STYLESHEETS)
def conversation_page():
  state = me.state(State)
  model_picker_dialog()
  with me.box(style=ROOT_BOX_STYLE):
    header()
    # me.text("len " + str(len(state.messages_by_model.items())))
    models = len(state.messages_by_model.items())
    models_px = models * 680
    with me.box(
      style=me.Style(
        width=f"min({models_px}px, calc(100% - 32px)",
        display="grid",
        gap=16,
        grid_template_columns=f"repeat({models}, 1fr)",
        flex_grow=1,
        overflow_y="hidden",
        margin=me.Margin.symmetric(horizontal="auto"),
        padding=me.Padding.symmetric(horizontal=16),
      )
    ):
      for model, messages in state.messages_by_model.items():
        with me.box(
          style=me.Style(
            overflow_y="auto",
          )
        ):
          me.text("Model: " + model, style=me.Style(font_weight=500))
          # TODO: remove this hack for lack of proper serialization
          state.messages_by_model[model] = messages = [
            ChatMessage(**message) if isinstance(message, dict) else message
            for message in messages
          ]
          for message in messages:
            if message.role == "user":
              user_message(message.content)
            else:
              model_message(message)
          if messages and model == list(state.messages_by_model.keys())[-1]:
            me.box(
              key="end_of_messages",
              style=me.Style(
                margin=me.Margin(
                  bottom="50vh" if messages[-1].in_progress else 0
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
