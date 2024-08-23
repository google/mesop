import hashlib
import os
import re
import urllib.parse
from os import getenv
from typing import NamedTuple

from flask import Flask, jsonify, request
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


@app.route("/save-interaction", methods=["POST"])
def save_interaction_endpoint():
  data = request.json
  assert data is not None
  prompt = data.get("prompt")
  before_code = data.get("beforeCode")
  diff = data.get("diff")
  if not prompt or not before_code or not diff:
    return jsonify({"error": "Invalid request"}), 400

  # Generate a unique folder name
  folder_name = generate_folder_name(prompt)
  base_path = "../ft/goldens"
  folder_path = os.path.join(base_path, folder_name)

  # Create the folder
  os.makedirs(folder_path, exist_ok=True)

  # Save prompt, before_code, and diff
  with open(os.path.join(folder_path, "prompt.txt"), "w") as f:
    f.write(prompt)
  with open(os.path.join(folder_path, "source.py"), "w") as f:
    f.write(before_code)
  with open(os.path.join(folder_path, "diff.txt"), "w") as f:
    f.write(diff)

  return jsonify({"folder": folder_name}), 200


@app.route("/adjust-mesop-app", methods=["POST"])
def adjust_mesop_app_endpoint():
  data = request.json
  assert data is not None
  code = data.get("code")
  prompt = data.get("prompt")

  if not code or not prompt:
    return jsonify({"error": "Both 'code' and 'prompt' are required"}), 400

  try:
    diff = adjust_mesop_app(code, prompt)
    result = apply_patch(code, diff)
    if result.has_error:
      raise Exception(result.result)
    return jsonify({"code": result.result, "diff": diff})
  except Exception as e:
    return jsonify({"error": str(e)}), 500


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
    original = original.strip()
    updated = updated.strip()

    # Replace the original part with the updated part
    new_patched_code = patched_code.replace(original, updated, 1)
    if new_patched_code == patched_code:
      return ApplyPatchResult(True, "WARN: DID_NOT_APPLY_PATCH")
    patched_code = new_patched_code

  return ApplyPatchResult(False, patched_code)


def adjust_mesop_app(code: str, msg: str) -> str:
  model = "ft:gpt-4o-mini-2024-07-18:personal::9yoxJtKf"
  client = OpenAI(
    api_key=getenv("OPENAI_API_KEY"),
  )
  return adjust_mesop_app_openai_client(code, msg, client, model=model)


def adjust_mesop_app_openai_client(
  code: str, msg: str, client: OpenAI, model: str
) -> str:
  completion = client.chat.completions.create(
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


def generate_folder_name(prompt: str) -> str:
  # Generate a unique 4-character suffix
  suffix = hashlib.md5(prompt.encode()).hexdigest()[:4]
  # Clean the prompt to create a valid folder name
  cleaned_prompt = urllib.parse.quote(prompt)[
    :50
  ]  # Limit to 50 chars and URL encode
  return f"{cleaned_prompt}_{suffix}"


if __name__ == "__main__":
  port = int(getenv("PORT", 43234))
  app.run(port=port)
