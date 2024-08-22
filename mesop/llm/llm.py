import datetime
import os
import re
from os import getenv
from typing import Literal, NamedTuple

import google.generativeai as genai
from google.generativeai import caching
from openai import OpenAI

from mesop.utils.runfiles import get_runfile_location

SYSTEM_INSTRUCTION_PART_1_PATH = get_runfile_location(
  "mesop/ai/ft/prompts/mesop_overview.txt"
)
SYSTEM_INSTRUCTION_PART_2_PATH = get_runfile_location(
  "mesop/ai/ft/prompts/mini_docs.txt"
)

with open(SYSTEM_INSTRUCTION_PART_1_PATH) as f:
  SYSTEM_INSTRUCTION_PART_1 = f.read()

with open(SYSTEM_INSTRUCTION_PART_2_PATH) as f:
  SYSTEM_INSTRUCTION_PART_2 = f.read()

SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTION_PART_1 + SYSTEM_INSTRUCTION_PART_2
PROMPT_PATH = get_runfile_location("mesop/ai/ft/prompts/revise_prompt.txt")

with open(PROMPT_PATH) as f:
  REVISE_APP_BASE_PROMPT = f.read().strip()

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


def make_gemini_model(model: str) -> genai.GenerativeModel:
  genai.configure(api_key=os.environ["GEMINI_FREE_API_KEY"])

  # cache = get_or_create_cache()
  # model = genai.GenerativeModel.from_cached_content(cached_content=cache)
  # return model
  return genai.GenerativeModel(
    model_name=model,  # "models/gemini-1.5-flash-001",
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings=safety_settings,
    generation_config=generation_config,
  )


def get_or_create_cache() -> caching.CachedContent:
  # prompt: get or create a cache
  cache_list = list(caching.CachedContent.list())
  if cache_list:
    cache_list[0]
    assert cache_list[0].display_name == "mesop_context"

    cache = cache_list[0]
    print("reuse existing cache", cache)
  else:
    cache = create_cache()
    print("create new cache", cache)
  return cache


def create_cache() -> caching.CachedContent:
  # Create a cache with a 5 minute TTL
  return caching.CachedContent.create(
    model="models/gemini-1.5-flash-001",
    display_name="mesop_context",  # used to identify the cache
    system_instruction=SYSTEM_INSTRUCTION,
    ttl=datetime.timedelta(minutes=10),
  )


class ApplyPatchResult(NamedTuple):
  has_error: bool
  result: str


def apply_patch(original_code: str, patch: str) -> ApplyPatchResult:
  # flash does some weird formatting.
  patch = patch.replace("```diff", "").replace("```", "")
  # Extract the diff content
  diff_pattern = r"<<<<<<< ORIGINAL(.*?)=======\n(.*?)>>>>>>> UPDATED"
  matches = re.findall(diff_pattern, patch, re.DOTALL)
  patched_code = original_code
  if len(matches) == 0:
    print("[WARN] No diff found:", patch)
    return ApplyPatchResult(True, "WARN: NO_DIFFS_FOUND")
  for original, updated in matches:
    original = original.strip()
    updated = updated.strip()

    # Replace the original part with the updated part
    new_patched_code = patched_code.replace(original, updated, 1)
    if new_patched_code == patched_code:
      return ApplyPatchResult(True, "WARN: DID_NOT_APPLY_PATCH")
    patched_code = new_patched_code

  return ApplyPatchResult(False, patched_code)


def adjust_mesop_app(
  code: str,
  msg: str,
  model=Literal[
    "gemini-pro",
    "gemini-flash",
    "deepseek",
    "sonnet",
    "gpt-4o-mini",
    "gpt-4o-mini-ft",
    "gpt-4o",
  ],
) -> str:
  model = "ft:gpt-4o-mini-2024-07-18:personal::9yoxJtKf"
  client = OpenAI(
    api_key=getenv("OPENAI_API_KEY"),
  )
  response = adjust_mesop_app_openai_client(code, msg, client, model=model)
  result = apply_patch(code, response)
  if result.has_error:
    raise Exception(result.result)
  return result.result


def adjust_mesop_app_openai_client(
  code: str, msg: str, client: OpenAI, model: str
) -> str:
  completion = client.chat.completions.create(
    #  model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    #  model = "deepseek-coder-v2",
    #  model="llama-3.1-70b-versatile",
    model=model,
    max_tokens=10_000,
    messages=[
      {
        "role": "system",
        "content": SYSTEM_INSTRUCTION,
      },
      {
        "role": "user",
        "content": REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
          "<APP_CHANGES>", msg
        ),
      },
    ],
  )
  print("[INFO] LLM output:", completion.choices[0].message.content)
  llm_output = completion.choices[0].message.content
  return llm_output
