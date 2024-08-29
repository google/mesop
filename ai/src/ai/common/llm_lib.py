import os
import re
from os import getenv
from typing import NamedTuple

import google.generativeai as genai
from openai import OpenAI
from openai.types.chat import (
  ChatCompletionMessageParam,
)

SYSTEM_INSTRUCTION_PART_1_PATH = "src/ai/prompts/mesop_overview.txt"
# SYSTEM_INSTRUCTION_PART_2_PATH = "src/ai/prompts/mini_docs.txt"

with open(SYSTEM_INSTRUCTION_PART_1_PATH) as f:
  SYSTEM_INSTRUCTION_PART_1 = f.read()

# with open(SYSTEM_INSTRUCTION_PART_2_PATH) as f:
#   SYSTEM_INSTRUCTION_PART_2 = f.read()

# Intentionally skip the more extensive system instruction with docs for now.
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTION_PART_1  # + SYSTEM_INSTRUCTION_PART_2
PROMPT_PATH = "src/ai/prompts/revise_prompt.txt"

with open(PROMPT_PATH) as f:
  REVISE_APP_BASE_PROMPT = f.read().strip()

EDIT_HERE_MARKER = " # <--- EDIT HERE"


class ApplyPatchResult(NamedTuple):
  has_error: bool
  result: str


def apply_patch(original_code: str, patch: str) -> ApplyPatchResult:
  # Extract the diff content
  diff_pattern = r"<<<<<<< ORIGINAL(.*?)=======\n(.*?)>>>>>>> UPDATED"
  matches = re.findall(diff_pattern, patch, re.DOTALL)
  patched_code = original_code
  if len(matches) == 0:
    print("[WARN] No diff found:", patch)
    return ApplyPatchResult(
      True,
      "[AI-001] Sorry! AI output was mis-formatted. Please try again.",
    )
  for original, updated in matches:
    original = original.strip().replace(EDIT_HERE_MARKER, "")
    updated = updated.strip().replace(EDIT_HERE_MARKER, "")

    # Replace the original part with the updated part
    new_patched_code = patched_code.replace(original, updated, 1)
    if new_patched_code == patched_code:
      print("[WARN] Diff did not update code:", patch)
      return ApplyPatchResult(
        True,
        "[AI-002] Sorry! AI output could not be used. Please try again.",
      )
    patched_code = new_patched_code

  return ApplyPatchResult(False, patched_code)


DEFAULT_MODEL = "ft:gpt-4o-mini-2024-07-18:mesop:small-prompt:A1472X3c"
DEFAULT_CLIENT = OpenAI(
  api_key=getenv("OPENAI_API_KEY"),
)


def format_messages(
  code: str, user_input: str, line_number: int | None
) -> list[ChatCompletionMessageParam]:
  # Add sentinel token based on line_number (1-indexed)
  if line_number is not None:
    code_lines = code.splitlines()
    if 1 <= line_number <= len(code_lines):
      code_lines[line_number - 1] += EDIT_HERE_MARKER
    code = "\n".join(code_lines)

  formatted_prompt = REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
    "<APP_CHANGES>", user_input
  )

  return [
    {"role": "system", "content": SYSTEM_INSTRUCTION},
    {"role": "user", "content": formatted_prompt},
  ]


def adjust_mesop_app_stream(
  *,
  code: str,
  user_input: str,
  line_number: int | None,
  client: OpenAI = DEFAULT_CLIENT,
  model: str = DEFAULT_MODEL,
):
  """
  Returns a stream of the code diff.
  """
  model = make_gemini_model()
  response = model.generate_content(
    REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
      "<APP_CHANGES>", user_input
    ),
    request_options={"timeout": 120},
    safety_settings=safety_settings,
    generation_config=generation_config,
    stream=True,
  )
  for chunk in response:
    yield chunk.text


def adjust_mesop_app_blocking(
  *,
  code: str,
  user_input: str,
  line_number: int | None = None,
  client: OpenAI = DEFAULT_CLIENT,
  model: str = DEFAULT_MODEL,
) -> str:
  """
  Returns the code diff.
  """
  return adjust_mesop_app_gemini(code, user_input)
  messages = format_messages(code, user_input, line_number)

  response = client.chat.completions.create(
    model=model,
    max_tokens=10_000,
    messages=messages,
    stream=False,
  )
  content = response.choices[0].message.content
  assert content is not None
  return content


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 32768,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]


def make_gemini_model() -> genai.GenerativeModel:
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  # cache = get_or_create_cache()
  # model = genai.GenerativeModel.from_cached_content(cached_content=cache)
  # return model
  return genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-001",
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings=safety_settings,
    generation_config=generation_config,
  )


def adjust_mesop_app_gemini(code: str, user_input: str) -> str:
  model = make_gemini_model()
  response = model.generate_content(
    REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
      "<APP_CHANGES>", user_input
    ),
    request_options={"timeout": 120},
    safety_settings=safety_settings,
    generation_config=generation_config,
  )

  llm_output = response.text.strip()
  print("[INFO] LLM output:", llm_output)
  return llm_output
