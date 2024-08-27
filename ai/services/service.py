import json
import os
import re
import secrets
import urllib.parse
from dataclasses import asdict, dataclass
from os import getenv
from typing import NamedTuple

from flask import Flask, Response, request, stream_with_context
from openai import OpenAI

app = Flask(__name__)

SYSTEM_INSTRUCTION_PART_1_PATH = "../ft/prompts/mesop_overview.txt"
SYSTEM_INSTRUCTION_PART_2_PATH = "../ft/prompts/mini_docs.txt"

with open(SYSTEM_INSTRUCTION_PART_1_PATH) as f:
  SYSTEM_INSTRUCTION_PART_1 = f.read()

with open(SYSTEM_INSTRUCTION_PART_2_PATH) as f:
  SYSTEM_INSTRUCTION_PART_2 = f.read()

SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTION_PART_1 + SYSTEM_INSTRUCTION_PART_2
PROMPT_PATH = "../ft/prompts/revise_prompt.txt"

with open(PROMPT_PATH) as f:
  REVISE_APP_BASE_PROMPT = f.read().strip()

EDIT_HERE_MARKER = " # <--- EDIT HERE"


@dataclass
class InteractionMetadata:
  line_number: int | None


@app.route("/save-interaction", methods=["POST"])
def save_interaction_endpoint() -> Response | dict[str, str]:
  data = request.json
  assert data is not None
  prompt = data.get("prompt")
  before_code = data.get("beforeCode")
  diff = data.get("diff")

  if not prompt or not before_code or not diff:
    return Response("Invalid request", status=400)

  line_number = data.get("lineNumber")
  if line_number is not None:
    metadata = InteractionMetadata(line_number=line_number)
  else:
    metadata = None
  folder_name = generate_folder_name(prompt)
  base_path = "../ft/goldens"
  folder_path = os.path.join(base_path, folder_name)

  os.makedirs(folder_path, exist_ok=True)

  with open(os.path.join(folder_path, "prompt.txt"), "w") as f:
    f.write(prompt)
  with open(os.path.join(folder_path, "source.py"), "w") as f:
    f.write(before_code)
  with open(os.path.join(folder_path, "diff.txt"), "w") as f:
    f.write(diff)
  if metadata is not None:
    with open(os.path.join(folder_path, "metadata.json"), "w") as f:
      json.dump(asdict(metadata), f)

  return {"folder": folder_name}


@app.route("/adjust-mesop-app", methods=["POST"])
def adjust_mesop_app_endpoint():
  data = request.json
  assert data is not None
  code = data.get("code")
  prompt = data.get("prompt")
  line_number = data.get("lineNumber")

  if not code or not prompt:
    return Response("Both 'code' and 'prompt' are required", status=400)

  def generate():
    stream = adjust_mesop_app(code, prompt, line_number)
    diff = ""
    for chunk in stream:
      if chunk.choices[0].delta.content:
        diff += chunk.choices[0].delta.content
        yield f"data: {json.dumps({'type': 'progress', 'data': chunk.choices[0].delta.content})}\n\n"

    result = apply_patch(code, diff)
    if result.has_error:
      raise Exception(result.result)

    yield f"data: {json.dumps({'type': 'end', 'code': result.result, 'diff': diff})}\n\n"

  return Response(
    stream_with_context(generate()), content_type="text/event-stream"
  )


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
    return ApplyPatchResult(True, "WARN: NO_DIFFS_FOUND")
  for original, updated in matches:
    original = original.strip().replace(EDIT_HERE_MARKER, "")
    updated = updated.strip().replace(EDIT_HERE_MARKER, "")

    # Replace the original part with the updated part
    new_patched_code = patched_code.replace(original, updated, 1)
    if new_patched_code == patched_code:
      return ApplyPatchResult(True, "WARN: DID_NOT_APPLY_PATCH")
    patched_code = new_patched_code

  return ApplyPatchResult(False, patched_code)


def adjust_mesop_app(code: str, msg: str, line_number: int | None):
  model = "accounts/willchen90-71c40c/models/98f31952c320416b899d0a8336662973"
  # client = OpenAI(
  #   api_key=getenv("OPENAI_API_KEY"),
  # )
  client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=getenv("FIREWORKS_API_KEY"),
  )

  # Add sentinel token based on line_number (1-indexed)
  if line_number is not None:
    code_lines = code.splitlines()
    if 1 <= line_number <= len(code_lines):
      code_lines[line_number - 1] += EDIT_HERE_MARKER
    code = "\n".join(code_lines)

  formatted_prompt = REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
    "<APP_CHANGES>", msg
  )

  return client.chat.completions.create(
    model=model,
    max_tokens=10_000,
    messages=[
      {
        "role": "system",
        "content": SYSTEM_INSTRUCTION,
      },
      {
        "role": "user",
        "content": formatted_prompt,
      },
    ],
    stream=True,
  )


def generate_folder_name(prompt: str) -> str:
  # Generate a unique 4-character suffix to avoid naming collisions
  suffix = secrets.token_urlsafe(4)
  cleaned_prompt = urllib.parse.quote(prompt)[:50]
  return f"{cleaned_prompt}_{suffix}"


if __name__ == "__main__":
  port = int(getenv("PORT", 43234))
  app.run(port=port)
