from os import getenv
from typing import Iterator

from openai import OpenAI
from openai.types.chat import (
  ChatCompletionMessageParam,
)

from ai.common.diff import EDIT_HERE_MARKER, ApplyPatchResult, apply_patch
from ai.common.entity_store import get_data_path
from ai.common.example import ExampleInput
from ai.common.model import model_store
from ai.common.producer import producer_store
from ai.common.prompt_context import prompt_context_store
from ai.common.prompt_fragment import PromptFragment, prompt_fragment_store


class ProviderExecutor:
  def __init__(self, model_name: str, prompt_fragments: list[PromptFragment]):
    self.model_name = model_name

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

    return [
      {
        "role": pf.role,
        "content": pf.content_value.replace("<APP_CODE>", code).replace(  # type: ignore
          "<APP_CHANGES>", input.prompt
        ),
      }
      for pf in self.prompt_fragments
    ]

  def execute(self, input: ExampleInput) -> str: ...

  def execute_stream(self, input: ExampleInput) -> Iterator[str]: ...


class OpenaiExecutor(ProviderExecutor):
  def __init__(self, model_name: str, prompt_fragments: list[PromptFragment]):
    super().__init__(model_name, prompt_fragments)
    self.client = OpenAI(
      api_key=getenv("OPENAI_API_KEY"),
    )

  def execute(self, input: ExampleInput) -> str:
    response = self.client.chat.completions.create(
      model=self.model_name,
      max_tokens=10_000,
      messages=self.format_messages(input),
    )
    return response.choices[0].message.content or ""

  def execute_stream(self, input: ExampleInput) -> Iterator[str]:
    stream = self.client.chat.completions.create(
      model=self.model_name,
      max_tokens=10_000,
      messages=self.format_messages(input),
      stream=True,
    )
    for chunk in stream:
      content = chunk.choices[0].delta.content
      yield content or ""


provider_executors: dict[str, type[ProviderExecutor]] = {
  "openai": OpenaiExecutor,
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
    provider_executor = provider_executor_type(model.name, prompt_fragments)
    return provider_executor

  def execute(self, input: ExampleInput):
    return self.get_provider_executor().execute(input)

  def execute_stream(self, input: ExampleInput):
    return self.get_provider_executor().execute_stream(input)

  def transform_output(self, input_code: str, output: str):
    if self.producer.output_format == "diff":
      return apply_patch(input_code, output)
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
