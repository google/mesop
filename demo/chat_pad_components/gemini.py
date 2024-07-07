import os

import google.generativeai as genai
from typing_extensions import TypedDict

from chat_pad_components.data_model import ChatMessage

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class Pad(TypedDict):
  title: str
  content: str


class Output(TypedDict):
  intro: str
  pad: Pad
  conclusion: str


# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
  # "response_schema": Output,
}


def send_prompt_pro(prompt: str, history: list[ChatMessage]):
  model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
      {"role": message.role, "parts": [message.content]} for message in history
    ]
  )

  for chunk in chat_session.send_message(prompt, stream=True):
    yield chunk.text


def send_prompt_flash(prompt: str, history: list[ChatMessage]):
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
      {"role": message.role, "parts": [message.content]} for message in history
    ]
  )

  for chunk in chat_session.send_message(prompt, stream=True):
    yield chunk.text
