"""
Formats the dataset for the fine-tuning process.
"""

import json
import os
from typing import Any

from llm_lib import REVISE_APP_BASE_PROMPT, SYSTEM_INSTRUCTION

EDIT_HERE_MARKER = " # <--- EDIT HERE"


def process_goldens():
  dataset: list[dict[str, Any]] = []
  outputs_dir = "goldens"

  for dir_name in os.listdir(outputs_dir):
    dir_path = os.path.join(outputs_dir, dir_name)
    if os.path.isdir(dir_path):
      prompt_path = os.path.join(dir_path, "prompt.txt")
      diff_path = os.path.join(dir_path, "diff.txt")
      line_number: int | None = None
      meta_path = os.path.join(dir_path, "metadata.json")
      if os.path.exists(meta_path):
        with open(meta_path) as meta_file:
          meta = json.load(meta_file)
          line_number = meta.get("line_number")
          print(f"line_number: {line_number}")

      with open(prompt_path) as prompt_file:
        prompt = prompt_file.read().strip()

      with open(diff_path) as diff_file:
        diff = diff_file.read().strip()

      code_path = os.path.join(dir_path, "source.py")
      if os.path.exists(code_path):
        with open(code_path) as code_file:
          code = code_file.read().strip()
      else:
        code = ""

        # Add sentinel token based on line_number (1-indexed)
      if line_number is not None:
        code_lines = code.splitlines()
        if 1 <= line_number <= len(code_lines):
          code_lines[line_number - 1] += EDIT_HERE_MARKER
        code = "\n".join(code_lines)

      formatted_prompt = REVISE_APP_BASE_PROMPT.replace(
        "<APP_CODE>", code
      ).replace("<APP_CHANGES>", prompt)

      dataset.append(
        {
          "messages": [
            {
              "role": "system",
              "content": SYSTEM_INSTRUCTION,
            },
            {
              "role": "user",
              "content": formatted_prompt,
            },
            {
              "role": "assistant",
              "content": diff,
            },
          ],
        }
      )

  return dataset


if __name__ == "__main__":
  formatted_dataset = process_goldens()
  print(f"Processed {len(formatted_dataset)} samples.")
  # create gen dir if it doesn't exist
  os.makedirs("./gen", exist_ok=True)
  # Append each sample as a JSON object on a separate line to a file
  with open("./gen/formatted_dataset.jsonl", "w") as f:
    for sample in formatted_dataset:
      f.write(json.dumps(sample) + "\n")
