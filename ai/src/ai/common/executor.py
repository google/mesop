import os
from hashlib import md5
from os import getenv
from typing import Iterable, Iterator

import google.generativeai as genai
from openai import OpenAI
from openai.types.chat import (
  ChatCompletionMessageParam,
)

from ai.common.diff import (
  EDIT_HERE_MARKER,
  ApplyPatchResult,
  apply_patch,
  apply_udiff,
)
from ai.common.entity_store import get_data_path
from ai.common.example import ExampleInput
from ai.common.model import model_store
from ai.common.producer import producer_store
from ai.common.prompt_context import prompt_context_store
from ai.common.prompt_fragment import PromptFragment, prompt_fragment_store


class ProviderExecutor:
  def __init__(
    self,
    model_name: str,
    prompt_fragments: list[PromptFragment],
    temperature: float,
  ):
    self.model_name = model_name
    self.temperature = temperature
    self.prompt_fragments = [
      PromptFragment(
        id=pf.id,
        role=pf.role,
        chain_of_thought=pf.chain_of_thought,
        content_value=get_content_value(pf),
        content_path=None,
      )
      for pf in prompt_fragments
    ]

  def format_messages(
    self, input: ExampleInput
  ) -> list[ChatCompletionMessageParam]:
    code = input.input_code or ""
    # Add sentinel token based on line_number (1-indexed)
    if input.line_number_target is not None:
      code_lines = code.splitlines()
      if 1 <= input.line_number_target <= len(code_lines):
        code_lines[input.line_number_target - 1] += EDIT_HERE_MARKER
      code = "\n".join(code_lines)

    messages = []
    current_role = None
    current_content = []

    for pf in self.prompt_fragments:
      content = pf.content_value.replace("<APP_CODE>", code).replace(
        "<APP_CHANGES>", input.prompt
      )

      if pf.role == current_role:
        current_content.append(content)
      else:
        if current_role is not None:
          messages.append(
            {"role": current_role, "content": "\n".join(current_content)}
          )
        current_role = pf.role
        current_content = [content]

    if current_role is not None:
      messages.append(
        {"role": current_role, "content": "\n".join(current_content)}
      )

    return messages

  def execute(self, input: ExampleInput, seed: int | None = None) -> str: ...

  def execute_stream(self, input: ExampleInput) -> Iterator[str]: ...


class OpenaiExecutor(ProviderExecutor):
  def __init__(
    self,
    model_name: str,
    prompt_fragments: list[PromptFragment],
    temperature: float,
  ):
    super().__init__(model_name, prompt_fragments, temperature)
    self.client = OpenAI(
      api_key=getenv("OPENAI_API_KEY"),
    )

  def execute(self, input: ExampleInput, seed: int | None = None) -> str:
    response = self.client.chat.completions.create(
      model=self.model_name,
      max_tokens=10_000,
      messages=self.format_messages(input),
      temperature=self.temperature,
      seed=seed,
    )
    return response.choices[0].message.content or ""

  def execute_stream(self, input: ExampleInput) -> Iterator[str]:
    stream = self.client.chat.completions.create(
      model=self.model_name,
      max_tokens=10_000,
      messages=self.format_messages(input),
      stream=True,
      temperature=self.temperature,
    )
    for chunk in stream:
      content = chunk.choices[0].delta.content
      yield content or ""


class FireworksExecutor(OpenaiExecutor):
  def __init__(
    self,
    model_name: str,
    prompt_fragments: list[PromptFragment],
    temperature: float,
  ):
    super().__init__(model_name, prompt_fragments, temperature)
    self.client = OpenAI(
      base_url="https://api.fireworks.ai/inference/v1",
      api_key=getenv("FIREWORKS_API_KEY"),
    )

  def execute(self, input: ExampleInput, seed: int | None = None) -> str:
    # Fireworks doesn't support seeding, so we ignore it.
    response = self.client.chat.completions.create(
      model=self.model_name,
      max_tokens=10_000,
      messages=self.format_messages(input),
      temperature=self.temperature,
    )
    return response.choices[0].message.content or ""


class TogetherExecutor(OpenaiExecutor):
  def __init__(
    self,
    model_name: str,
    prompt_fragments: list[PromptFragment],
    temperature: float,
  ):
    super().__init__(model_name, prompt_fragments, temperature)
    self.client = OpenAI(
      base_url="https://api.together.xyz/v1",
      api_key=getenv("TOGETHER_API_KEY"),
    )


class GeminiExecutor(ProviderExecutor):
  def __init__(
    self,
    model_name: str,
    prompt_fragments: list[PromptFragment],
    temperature: float,
  ):
    super().__init__(model_name, prompt_fragments, temperature)
    genai.configure(api_key=getenv("GOOGLE_API_KEY"))  # type: ignore

  def execute_stream(self, input: ExampleInput) -> Iterator[str]:
    contents = self._format_gemini_messages(self.format_messages(input))
    client = self._make_client()
    for response in client.generate_content(contents, stream=True):  # type: ignore
      yield response.text

  def execute(self, input: ExampleInput, seed: int | None = None):
    # Gemini doesn't support seeding, so we ignore it.
    # https://github.com/GoogleCloudPlatform/generative-ai/issues/289
    contents = self._format_gemini_messages(self.format_messages(input))
    client = self._make_client()
    return client.generate_content(contents).text  # type: ignore

  def _make_client(self) -> genai.GenerativeModel:
    return genai.GenerativeModel(
      model_name=self.model_name,
      generation_config={
        "temperature": self.temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 10_000,
        "response_mime_type": "text/plain",
      },  # type: ignore
    )

  def _format_gemini_messages(
    self, messages: Iterable[ChatCompletionMessageParam]
  ) -> Iterable[str]:
    contents: list[str] = []
    for message in messages:
      if message["role"] == "system":
        contents.append(message["content"])  # type: ignore
      elif message["role"] == "user":
        contents.append("input: " + str(message["content"]))
      elif message["role"] == "assistant" and "content" in message:
        contents.append("output: " + str(message["content"]))
    return contents


provider_executors: dict[str, type[ProviderExecutor]] = {
  "openai": OpenaiExecutor,
  "fireworks": FireworksExecutor,
  "together": TogetherExecutor,
  "gemini": GeminiExecutor,
}


class ProducerExecutor:
  def __init__(self, producer_id: str):
    self.producer = producer_store.get(producer_id)

  def get_provider_executor(self) -> ProviderExecutor:
    prompt_context = prompt_context_store.get(self.producer.prompt_context_id)
    prompt_fragments = [
      prompt_fragment_store.get(pfid) for pfid in prompt_context.fragment_ids
    ]
    model = model_store.get(self.producer.mesop_model_id)
    provider_executor_type = provider_executors.get(model.provider)
    if provider_executor_type is None:
      raise ValueError(f"Provider {model.provider} not supported")
    provider_executor = provider_executor_type(
      model.name, prompt_fragments, temperature=self.producer.temperature
    )
    return provider_executor

  def execute(self, input: ExampleInput, seed: int | None = None):
    provider_executor = self.get_provider_executor()
    if seed is None:
      return provider_executor.execute(input, seed=seed)

    # Create a unique cache key
    cache_key = md5(
      f"{self.producer}:{provider_executor.format_messages(input)}:{seed}".encode()
    ).hexdigest()
    cache_dir = os.path.join(get_data_path(".cache"))
    cache_file = os.path.join(cache_dir, cache_key)

    # Check if cached result exists
    if os.path.exists(cache_file):
      with open(cache_file) as f:
        return f.read()

    # Execute and cache the result
    output = provider_executor.execute(input, seed=seed)
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, "w") as f:
      f.write(output)

    return output

  def execute_stream(self, input: ExampleInput):
    return self.get_provider_executor().execute_stream(input)

  def transform_output(self, input_code: str, output: str):
    if self.producer.output_format == "diff":
      return apply_patch(input_code, output)
    elif self.producer.output_format == "udiff":
      return apply_udiff(input_code, output)
    elif self.producer.output_format == "full":
      return ApplyPatchResult(True, output)
    else:
      raise ValueError(f"Unknown output format: {self.producer.output_format}")


def get_content_value(pf: PromptFragment) -> str | None:
  if pf.content_value is not None:
    return pf.content_value
  if pf.content_path is not None:
    with open(get_data_path(pf.content_path.replace("//", ""))) as f:
      return f.read()
  return None
