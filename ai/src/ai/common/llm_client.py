from os import getenv
from typing import Iterable, Protocol

import google.generativeai as genai
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

genai.configure(api_key=getenv("GOOGLE_API_KEY"))


class LlmClient(Protocol):
  def generate_content_stream(
    self,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int,
  ):
    raise NotImplementedError()

  def generate_content_blocking(
    self,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int,
  ):
    raise NotImplementedError()


class OpenAIClient(LlmClient):
  def __init__(self) -> None:
    self.client = OpenAI(
      api_key=getenv("OPENAI_API_KEY"),
    )

  def generate_content_stream(
    self,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int,
  ):
    response = self.client.chat.completions.create(
      model=model,
      max_tokens=max_tokens,
      messages=messages,
      stream=True,
    )
    for chunk in response:
      if chunk.choices[0].delta.content:
        yield chunk.choices[0].delta.content

  def generate_content_blocking(
    self,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int,
  ):
    response = self.client.chat.completions.create(
      model=model,
      max_tokens=max_tokens,
      messages=messages,
      stream=False,
    )
    content = response.choices[0].message.content
    assert content is not None
    return content


class GeminClient(LlmClient):
  def generate_content_stream(
    self,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int,
  ):
    contents = self._make_messages(messages)
    client = self._make_client(model, max_tokens)
    for response in client.generate_content(contents, stream=True):
      yield response.text

  def generate_content_blocking(
    self,
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    max_tokens: int,
  ):
    contents = self._make_messages(messages)
    client = self._make_client(model, max_tokens)
    return client.generate_content(contents).text

  def _make_client(self, model: str, max_tokens: int) -> genai.GenerativeModel:
    return genai.GenerativeModel(
      model_name=model,
      generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
      },  # type: ignore
    )

  def _make_messages(
    self, messages: Iterable[ChatCompletionMessageParam]
  ) -> Iterable[str]:
    contents = []
    for message in messages:
      if message["role"] == "system":
        contents.append(message["content"])
      elif message["role"] == "user":
        contents.append("input: " + str(message["content"]))
      elif message["role"] == "assistant" and "content" in message:
        contents.append("output: " + str(message["content"]))
    return contents
